from fastapi import Depends, Request
from fastapi_permissions import (
    Allow,
    Authenticated,
    Everyone,
    configure_permissions,
    has_permission,
)

from app.api.endpoints.dependencies import get_auth_user_controller
from app.controllers import AuthUserController
from app.core.exceptions import Forbidden, Unauthorized
from app.database.base import Base
from app.models import AuthUser

PROFILE_COMPLETE = "profile_complete"
SUPER_ADMIN_USER = "super_admin_user"


def get_active_principals(
    request: Request,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
):
    auth_user: AuthUser = request.state.auth_user
    principals = [Everyone]

    if auth_user:
        principals.append(Authenticated)
        _add_super_admin_principal(principals, auth_user)
        _add_auth_user_principal(principals, auth_user)

    return principals


def assert_allowed_on_resource(principals: list[str], action: str, resource: Base):
    if not has_permission(principals, action, resource):
        raise Forbidden("Not authorized to perform this action.")


def assert_allowed_on_collection(
    principals: list[str], action: str, collection: list[Base]
):
    for resource in collection:
        assert_allowed_on_resource(principals, action, resource)


def _add_super_admin_principal(principals: list[str], auth_user: AuthUser):
    if auth_user.is_admin:
        principals.append(SUPER_ADMIN_USER)


def _add_auth_user_principal(principals: list[str], auth_user: AuthUser):
    if auth_user:
        principals.append(f"auth_user:{auth_user.id}")

        if auth_user.is_profile_complete:
            principals.append(PROFILE_COMPLETE)


Permission = configure_permissions(
    get_active_principals, permission_exception=Unauthorized
)

AuthenticatedAccess = [(Allow, Authenticated, "access_endpoint")]
CompleteUserAccess = [(Allow, PROFILE_COMPLETE, "access_endpoint")]
SuperAdminAccess = [(Allow, SUPER_ADMIN_USER, "access_endpoint")]
