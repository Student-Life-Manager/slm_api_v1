from fastapi import APIRouter, Depends, Request

from app.api.endpoints.dependencies.controllers import get_auth_user_controller
from app.api.endpoints.dependencies.permissions import admin_required, auth_required
from app.controllers import AuthUserController
from app.schema import (
    AuthUserAccountType,
    AuthUserCreate,
    AuthUserRegisterReturn,
    AuthUserReturn,
)

router = APIRouter(prefix="/wardens")


@router.post("/register", response_model=AuthUserRegisterReturn)
@auth_required
@admin_required
def create_new_warden(
    request: Request,
    auth_user_create: AuthUserCreate,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Create new users
    """
    auth_user = auth_user_controller.register(
        auth_user_create, AuthUserAccountType.WARDEN
    )

    return auth_user


@router.get("/", response_model=list[AuthUserReturn])
@auth_required
def get_all_wardens(
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Returns all auth_users with role as wardens
    """

    wardens = auth_user_controller.get_wardens()

    return wardens
