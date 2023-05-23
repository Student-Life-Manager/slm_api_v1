"""
permissions
"""
from functools import wraps

from fastapi import Request

from app.controllers.auth import AuthUserController
from app.core.exceptions import BadRequest, Unauthorized
from app.core.jwt import JWTHandler
from app.crud.auth_user import CRUDAuthUser
from app.database.session import SessionLocal
from app.models.auth_user import AuthUser
from app.schema.auth_user import AuthUserAccountType


def auth_required(func):
    """
    auth decorator acting as a middleware to fetch user id from token
    """

    # the below line declares auth_required as a decorator
    @wraps(func)
    def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        elif "Auth" in request.headers:
            token = request.headers["Auth"]
        elif "X-Authorization" in request.headers:
            token = request.headers["X-Authorization"]

        if not token:
            raise Unauthorized(message="Missing bearer token.")

        user_id = validate_token(token.split(" ")[1])

        request.state.auth_user_id = user_id
        auth_user = AuthUserController(
            db=SessionLocal(),
            crud_auth_user=CRUDAuthUser(db=SessionLocal(), model=AuthUser),
        ).get(user_id)

        request.state.auth_user = auth_user

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    @auth_required
    def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]

        auth_user: AuthUser = request.state.auth_user

        if not auth_user:
            raise BadRequest("No auth user found.")

        if not auth_user.is_admin:
            raise Unauthorized("Unauthorized.")

        return func(*args, **kwargs)

    return wrapper


def warden_route(func):
    @wraps(func)
    @auth_required
    def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]

        auth_user: AuthUser = request.state.auth_user

        if not auth_user:
            raise BadRequest("No auth user found.")

        if auth_user.account_type != AuthUserAccountType.WARDEN:
            raise Unauthorized("Unauthorized.")

        return func(*args, **kwargs)

    return wrapper


def student_route(func):
    @wraps(func)
    @auth_required
    def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]

        auth_user: AuthUser = request.state.auth_user

        if not auth_user:
            raise BadRequest("No auth user found.")

        if auth_user.account_type != AuthUserAccountType.STUDENT:
            raise Unauthorized("Unauthorized.")

        return func(*args, **kwargs)

    return wrapper


def guard_route(func):
    @wraps(func)
    @auth_required
    def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]

        auth_user: AuthUser = request.state.auth_user

        if not auth_user:
            raise BadRequest("No auth user found.")

        if auth_user.account_type != AuthUserAccountType.GUARD:
            raise Unauthorized("Unauthorized.")

        return func(*args, **kwargs)

    return wrapper


def validate_token(access_token: str) -> int:
    """
    validate and decode access_token
    """
    payload = JWTHandler.decode(token=access_token)
    user_id = payload["auth_user_id"]

    if not user_id:
        raise BadRequest("Not authorized.")

    return user_id
