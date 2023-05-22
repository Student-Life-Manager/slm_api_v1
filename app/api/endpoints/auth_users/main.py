from fastapi import APIRouter, Depends, Request

from app.api.endpoints.dependencies.controllers import get_auth_user_controller
from app.api.endpoints.dependencies.permissions import auth_required
from app.controllers import AuthUserController
from app.schema import (
    AuthUserAuthRefresh,
    AuthUserLoggedInReturn,
    AuthUserLogin,
    AuthUserPasswordUpdate,
    AuthUserReturn,
    AuthUserTokenReturn,
    AuthUserUpdate,
)

router = APIRouter(prefix="/auth_users")


@router.post("/login", response_model=AuthUserLoggedInReturn)
def login(
    auth_user_login: AuthUserLogin,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Logins new user
    """

    jwt_token = auth_user_controller.login(
        email=auth_user_login.email, password=auth_user_login.password
    )

    return jwt_token


@router.patch("/me/password", response_model=bool)
@auth_required
def update_profile_details(
    request: Request,
    auth_user_password_update: AuthUserPasswordUpdate,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Adds profile details for auth users (can be used in both onboarding and edit profile pages)
    """

    auth_user = auth_user_controller.get(request.state.auth_user_id)

    if auth_user_controller.update_password(
        auth_user=auth_user, password=auth_user_password_update.password
    ):
        return True

    return False


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


@router.patch("/onboarding", response_model=AuthUserReturn)
@auth_required
def update_my_profile(
    auth_user_update: AuthUserUpdate,
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    auth_user = auth_user_controller.get(request.state.auth_user_id)

    updated_auth_user = auth_user_controller.update_profile(auth_user, auth_user_update)

    return updated_auth_user


@router.post("/me/auth", response_model=AuthUserTokenReturn)
def get_refresh_auth(
    auth_user_auth_refresh: AuthUserAuthRefresh,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Refresh tokens for auth_user
    """

    tokens = auth_user_controller.assign_new_access_token(
        access_token=auth_user_auth_refresh.access_token,
        refresh_token=auth_user_auth_refresh.refresh_token,
    )

    return tokens
