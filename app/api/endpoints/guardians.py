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
from app.schema import GuardianCreate, GuardianReturn, VerificationCodeReturn, AddGuardiansWithStudentEmail

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
    print("________student id_______", student.id)

    if not student:
        raise NotFound(message="No user found.")

    guardian = guardian_controller.create(
        guardian_create=guardian_create, student_id=request.state.auth_user_id,
    )

    return guardian



@router.post("/add_guardians", response_model=bool)
def add_bulk_guardian(
    new_guardians: list[AddGuardiansWithStudentEmail],
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    print(new_guardians)
    return guardian_controller.create_beautiful_guardians(new_guardians)




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


@router.get("/{guardian_uuid}/code", response_model=VerificationCodeReturn)
@auth_required
def get_guardian_otp(
    guardian_uuid: UUID,
    request: Request,
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    student_id = request.state.auth_user_id
    guardian = guardian_controller.get_guardian_with_student_id_and_uuid(
        student_id=student_id, guardian_uuid=guardian_uuid
    )

    return guardian_controller.send_guardian_verification_message(
        auth_user=request.state.auth_user, guardian=guardian
    )


@router.patch("/{guardian_uuid}/verify")
def verify_guardian(
    guardian_uuid: UUID,
    code: str,
    request: Request,
    guardian_controller: GuardianController = Depends(get_guardian_controller),
):
    """
    Verifies if the guardian is a proper guardian of the student
    """

    guardian = guardian_controller.verify_guardian(
        guardian_uuid=guardian_uuid, code=code
    )

    return guardian

# @router.get("/unverified/all")
# def get_all_unverified_guardians(request: Request):
#     """
#     Returns a list of all unverified guardians
#     """



