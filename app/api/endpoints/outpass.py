from uuid import UUID

from fastapi import APIRouter, Depends, Request

from app.api.endpoints.dependencies import (
    admin_required,
    auth_required,
    get_auth_user_controller,
    get_outpass_controller,
    student_route,
    warden_route,
    get_guardian_controller
)
from app.controllers import AuthUserController, OutpassController, GuardianController
from app.core.exceptions import BadRequest, NotFound
from app.schema import AuthUserAccountType, OutpassCreate, OutpassReturn

router = APIRouter(prefix="/outpass")


@router.post("/")
@student_route
def create_outpass(
    request: Request,
    warden_uuid : UUID,
    guardian_uuid: UUID,
    outpass_create: OutpassCreate,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
    outpass_controller: OutpassController = Depends(get_outpass_controller),
    guardian_controller : GuardianController = Depends(get_guardian_controller)
):
    """
    Returns all the outpasses of an auth user (students and wardens)
    """

    auth_user = auth_user_controller.get(request.state.auth_user_id)
    warden = auth_user_controller.get_by_uuid(warden_uuid)
    if not warden:
        raise NotFound("Warden does not exist")
    guardian = guardian_controller.get_by_uuid(guardian_uuid)
    if not guardian:
        raise NotFound("Guardian does not exist")
    
    outpass = outpass_controller.create(
        auth_user=auth_user, warden_id=warden.id, guardian_id=guardian.id, outpass_create=outpass_create
    )

    return outpass


@router.get("/")
@admin_required
def get_new_outpass(
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    """
    Adds a new outpass
    """

    outpasses = outpass_controller.get_multi()

    return outpasses


@router.get("/me", response_model=list[OutpassReturn])
@auth_required
def get_my_outpasses(
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    auth_user = request.state.auth_user

    if auth_user.account_type == AuthUserAccountType.STUDENT:
        return outpass_controller.get_student_outpasses(auth_user.id)

    if auth_user.account_type == AuthUserAccountType.WARDEN:
        return outpass_controller.get_warden_outpasses(auth_user.id)

    raise BadRequest(f"Incorrect auth_user type found: {auth_user.account_type}")


@router.get("/approved/me", response_model=list[OutpassReturn])
@warden_route
def get_approved_outpasses(
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    auth_user = request.state.auth_user

    return outpass_controller.get_warden_approved_outpasses(auth_user.id)


@router.patch("/{outpass_uuid}/approve", response_model=OutpassReturn)
@warden_route
def approve_outpass(
    outpass_uuid: UUID,
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    """
    Returns all the details of an outpass
    """
    warden = request.state.auth_user

    outpass = outpass_controller.get_by_uuid(outpass_uuid)

    if not outpass:
        raise NotFound("Outpass not found.")

    approved_outpass = outpass_controller.approve_first_level_outpass(
        warden=warden, outpass=outpass
    )

    return approved_outpass


@router.get("/{outpass_uuid}", response_model=OutpassReturn)
@auth_required
def get_outpass_details(
    outpass_uuid: UUID,
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    """
    Returns all the details of an outpass
    """
    auth_user_id = request.state.auth_user_id

    outpass = outpass_controller.get_outpass_by_student_id_and_uuid(
        student_id=auth_user_id, uuid=outpass_uuid
    )

    return outpass

@router.patch("/{outpass_uuid}", response_model=OutpassReturn)
@auth_required
def get_outpass_details(
    outpass_uuid: UUID,
    request: Request,
    outpass_controller: OutpassController = Depends(get_outpass_controller),
):
    """
    Returns all the details of an outpass
    """
    auth_user_id = request.state.auth_user_id

    outpass = outpass_controller.get_outpass_by_student_id_and_uuid(
        student_id=auth_user_id, uuid=outpass_uuid
    )

    return outpass
