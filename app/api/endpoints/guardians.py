from uuid import UUID

from fastapi import APIRouter, Depends, Request

from app.api.endpoints.dependencies import (
    admin_required,
    auth_required,
    get_auth_user_controller,
    get_guardian_controller,
)
from app.controllers import AuthUserController, GuardianController
from app.core.exceptions import NotFound
from app.schema import GuardianCreate, GuardianReturn

router = APIRouter(prefix="/guardians")


@router.get("/")
@auth_required
@admin_required
def get_all_guardians(
    request: Request,
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    """
    Returns all guardians of a student
    """

    guardians = guardian_controller.get_guardians()

    return guardians


@router.post("/", response_model=GuardianReturn)
@auth_required
def add_new_guardian(
    request: Request,
    guardian_create: GuardianCreate,
    auth_user_controller: AuthUserController = Depends(get_auth_user_controller),
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    """
    Add a new guardian for a student
    """

    student = auth_user_controller.get(request.state.auth_user_id)

    if not student:
        raise NotFound(message="No user found.")

    guardian = guardian_controller.create(
        guardian_create=guardian_create, student_id=student.id
    )

    return guardian


@router.get("/me", response_model=list[GuardianReturn])
@auth_required
def get_my_guardians(
    request: Request,
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    """
    Get student guardians
    """

    guardians = guardian_controller.get_student_guardians(request.state.auth_user_id)

    return guardians


@router.delete("/{guardian_uuid}")
@auth_required
def remove_guardian(
    request: Request,
    guardian_uuid: UUID,
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    """
    Removing a guardian for a student
    """

    return guardian_controller.delete(
        student_id=request.state.auth_user_id, guardian_uuid=guardian_uuid
    )


@router.patch("/{guardian_uuid}/verify")
@auth_required
@admin_required
def verify_guardian(
    guardian_uuid: UUID,
    request: Request,
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    """
    Verifies if the guardian is a proper guardian of the student
    """

    guardian = guardian_controller.verify_guardian(guardian_uuid)

    return guardian
