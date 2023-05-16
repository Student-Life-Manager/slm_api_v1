from pydantic import EmailStr

from app.core.config import settings
from app.core.exceptions import BadRequest, Unauthorized
from app.core.jwt import JWTHandler
from app.core.password import PasswordHandler
from app.crud import CRUDAuthUser
from app.models import AuthUser
from app.schema.auth_user import (
    AuthUserAccountType,
    AuthUserCreate,
    AuthUserHostelDetails,
    AuthUserRegisterReturn,
    AuthUserTokenReturn,
    AuthUserUpdate,
    StudentAcademicDetails,
    StudentChecklist,
    WardenChecklist,
)

from .base import BaseController


class AuthUserController(
    BaseController[
        AuthUser,
        None,
    ]
):
    def __init__(self, db, crud_auth_user: CRUDAuthUser):
        super().__init__(model=AuthUser, db=db, crud_instance=crud_auth_user)
        self.crud_auth_user = crud_auth_user

    def register(
        self, create_auth_user: AuthUserCreate, user_type: AuthUserAccountType
    ) -> AuthUserRegisterReturn:
        auth_user = self.crud_auth_user.get_by_email(create_auth_user.email)
        if auth_user:
            raise BadRequest("auth user already exists")

        password = PasswordHandler.hash(create_auth_user.password)
        attributes = self.extract_attributes_from_schema(create_auth_user)
        attributes["password"] = password
        attributes["account_type"] = user_type
        attributes["hostel_details"] = AuthUserHostelDetails().__dict__
        if user_type == AuthUserAccountType.STUDENT:
            attributes["checklist"] = StudentChecklist().__dict__
            attributes["academic_details"] = StudentAcademicDetails().__dict__

        elif user_type == AuthUserAccountType.WARDEN:
            attributes["checklist"] = WardenChecklist().__dict__
            attributes["academic_details"] = None

        new_user = self.crud_auth_user.create(attributes)
        authorization_token = {
            "access_token": JWTHandler.encode({"auth_user_id": new_user.id}),
            "refresh_token": JWTHandler.encode(
                {"auth_user_id": new_user.id, "sub": "refresh_token"},
                settings.AUTH_CONFIG.JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS,
            ),
        }
        student_user_register = AuthUserRegisterReturn(
            email=new_user.email,
            access_token=authorization_token["access_token"],
            refresh_token=authorization_token["refresh_token"],
        )
        return student_user_register

    def login(self, email: str, password: str):
        auth_user = self.crud_auth_user.get_by_email(email)
        if not auth_user:
            raise BadRequest("No account exists with this email")
        if not PasswordHandler.verify(auth_user.password, password):
            raise Unauthorized("Password provided is incorrect")

        return {
            "access_token": JWTHandler.encode({"auth_user_id": auth_user.id}),
            "refresh_token": JWTHandler.encode(
                {"auth_user_id": auth_user.id, "sub": "refresh_token"},
                settings.AUTH_CONFIG.JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS,
            ),
        }

    def update(
        self, auth_user: AuthUser, auth_user_update: AuthUserUpdate
    ) -> AuthUserUpdate:
        attributes = self.extract_attributes_from_schema(auth_user_update)

        return self.crud_auth_user.update(model=auth_user, attributes=attributes)

    def update_profile(self, auth_user: AuthUser, auth_user_update: AuthUserUpdate):
        attributes = self.extract_attributes_from_schema(auth_user_update)
        updated_auth_user = self.crud_auth_user.update(auth_user, attributes)

        self.update_auth_user_onboarding(updated_auth_user)

        return updated_auth_user

    def assign_new_access_token(
        self, access_token: str, refresh_token: str
    ) -> AuthUserTokenReturn:
        auth_user_id = self._check_refresh_token_validity(access_token, refresh_token)

        return {
            "access_token": JWTHandler.encode({"auth_user_id": auth_user_id}),
            "refresh_token": JWTHandler.encode(
                {"auth_user_id": auth_user_id, "sub": "refresh_token"},
                settings.AUTH_CONFIG.JWT_REFRESH_TOKEN_EXPIRY_IN_DAYS,
            ),
        }

    def update_password(self, auth_user: AuthUser, password: str) -> bool:
        hashed_password = PasswordHandler.hash(password)
        attributes = {"password": hashed_password}

        self.crud_auth_user.update(model=auth_user, attributes=attributes)

        return True

    def update_auth_user_onboarding(self, auth_user: AuthUser) -> None:
        checklist_db = auth_user.checklist

        for key in checklist_db:
            if not checklist_db[key]:
                allowed_step = key
                break

            if checklist_db[key]:
                continue

        if auth_user.account_type == AuthUserAccountType.STUDENT:
            valid_steps = self._checklist_step_validity_for_student(auth_user)
        elif auth_user.account_type == AuthUserAccountType.WARDEN:
            valid_steps = self._checklist_step_validity_for_warden(auth_user)

        for valid_step in valid_steps:
            checklist_db[valid_step] = True

        attributes = {"checklist": checklist_db}

        self.crud_auth_user.update(auth_user, attributes)

    def get_by_email(self, email: EmailStr) -> AuthUser | None:
        return self.crud_auth_user.get_by_email(email)

    def get_students(self) -> list[AuthUser]:
        return self.crud_auth_user.get_students()

    def get_wardens(self) -> list[AuthUser]:
        return self.crud_auth_user.get_wardens()

    def get_wardens_by_hostel_type(self, hostel_type: str) -> list[AuthUser]:
        return self.crud_auth_user.get_wardens_by_hostel_type(hostel_type=hostel_type)

    def _check_refresh_token_validity(
        self, access_token: str, refresh_token: str
    ) -> int:
        refresh_payload = JWTHandler.decode(refresh_token)
        payload = JWTHandler.decode_expire(access_token)

        if "sub" in refresh_payload and refresh_payload["sub"] != "refresh_token":
            raise BadRequest("Invalid refresh token.")

        if payload["auth_user_id"] != refresh_payload["auth_user_id"]:
            raise BadRequest("Access token and refresh token does not match.")

        return payload["auth_user_id"]

    def _checklist_step_validity_for_student(self, auth_user: AuthUser) -> list[str]:
        valid_steps = []
        if all(
            [
                auth_user.first_name,
                auth_user.last_name,
                auth_user.roll_number,
                auth_user.phone_number,
                auth_user.email,
            ]
        ):
            valid_steps.append("personal_details")

        if all(
            [
                auth_user.hostel_details["bldg_name"]
                if hasattr(auth_user, "hostel_details")
                else False,
                auth_user.hostel_details["room_no"]
                if hasattr(auth_user, "hostel_details")
                else False,
            ]
        ):
            valid_steps.append("hostel_details")

        if all(
            [
                auth_user.academic_details["year_of_study"] is not None,
                auth_user.academic_details["course"],
                auth_user.academic_details["branch"],
                auth_user.academic_details["section"],
            ]
        ):
            valid_steps.append("academic_details")

        return valid_steps

    def _check_refresh_token_validity(
        self, access_token: str, refresh_token: str
    ) -> int:
        refresh_payload = JWTHandler.decode(refresh_token)
        payload = JWTHandler.decode_expire(access_token)

        if "sub" in refresh_payload and refresh_payload["sub"] != "refresh_token":
            raise BadRequest("Invalid refresh token.")

        if payload["auth_user_id"] != refresh_payload["auth_user_id"]:
            raise BadRequest("Access token and refresh token does not match.")

        return payload["auth_user_id"]

    def _checklist_step_validity_for_warden(self, auth_user: AuthUser) -> list[str]:
        valid_steps = []
        if all(
            [
                auth_user.first_name,
                auth_user.last_name,
                auth_user.roll_number,
                auth_user.phone_number,
                auth_user.email,
            ]
        ):
            valid_steps.append("personal_details")

        if all(
            [
                auth_user.hostel_details["hostel_type"]
                if hasattr(auth_user, "hostel_details")
                else False,
                auth_user.hostel_details["bldg_name"]
                if hasattr(auth_user, "hostel_details")
                else False,
            ]
        ):
            valid_steps.append("hostel_details")

        return valid_steps
