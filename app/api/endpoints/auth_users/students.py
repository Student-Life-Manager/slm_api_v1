from fastapi import APIRouter, Depends, Request

from app.api.endpoints.dependencies.controllers import (
    get_auth_user_controller,
    get_outpass_controller,
)
from app.api.endpoints.dependencies.permissions import admin_required, auth_required
from app.controllers import AuthUserController, OutpassController
from app.core.exceptions import BadRequest
from app.schema import (
    AuthUserAccountType,
    AuthUserCreate,
    AuthUserHomeReturn,
    AuthUserRegisterReturn,
    AuthUserReturn,
    AuthUserUpdate,
)

router = APIRouter(prefix="/students")


@router.post("/register", response_model=AuthUserRegisterReturn)
def create_new_user(
    auth_user_create: AuthUserCreate,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Create new users
    """
    existing_auth_user = auth_user_controller.get_by_email(auth_user_create.email)

    if existing_auth_user:
        raise BadRequest(message="Auth user already exists with this email.")

    

    auth_user = auth_user_controller.register(
        auth_user_create, AuthUserAccountType.STUDENT
    )

    return auth_user


@router.get("/home", response_model=AuthUserHomeReturn)
@auth_required
def get_student_home(
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    auth_user = request.state.auth_user

    outpasses = outpass_controller.get_student_outpasses(auth_user.id)

    return AuthUserHomeReturn(auth_user=auth_user, outpass=outpasses)


@router.get("/", response_model=list[AuthUserReturn])
def get_all_students(
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Returns all auth_users with role as student
    """
    students = auth_user_controller.get_students()

    return students


@router.patch("/me/onboarding", response_model=AuthUserReturn)
@auth_required
def update_my_profile(
    auth_user_update: AuthUserUpdate,
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    auth_user = auth_user_controller.get(request.state.auth_user_id)

    updated_auth_user = auth_user_controller.update_profile(auth_user, auth_user_update)

    return updated_auth_user


@router.get("/me", response_model=AuthUserReturn)
@auth_required
def get_profile_details(
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Returns all details of an auth_user
    """

    auth_user = auth_user_controller.get(request.state.auth_user_id)

    return auth_user


@router.patch("/me", response_model=AuthUserReturn)
@auth_required
def update_me(
    auth_user_update: AuthUserUpdate,
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    auth_user = auth_user_controller.get(request.state.auth_user_id)

    return auth_user_controller.update(
        auth_user=auth_user, auth_user_update=auth_user_update
    )


