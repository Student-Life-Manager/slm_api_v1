from fastapi import APIRouter, Depends, Request

from app.api.endpoints.dependencies.controllers import (
    get_auth_user_controller,
    get_outpass_controller,
)
from app.controllers import AuthUserController
from app.schema import AuthUserAccountType, AuthUserCreate, AuthUserRegisterReturn

router = APIRouter(prefix="/guards")


@router.post("/register", response_model=AuthUserRegisterReturn)
def create_new_user(
    auth_user_create: AuthUserCreate,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    """
    Create new guard account
    """

    existing_auth_user = auth_user_controller.get_by_email(auth_user_create.email)

    if existing_auth_user:
        raise BadRequest(message="Auth user already exisits with this email")

    guard = auth_user_controller.register(auth_user_create, AuthUserAccountType.GUARD)
    return guard
