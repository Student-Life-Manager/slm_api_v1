from fastapi import APIRouter, Request, Depends

from app.api.endpoints.dependencies import get_auth_user_controller, get_guardian_controller, get_outpass_controller
from app.controllers import AuthUserController, GuardianController, OutpassController

router = APIRouter(prefix="/logs")


@router.get("/health", status_code=200)
def get_api_health(request: Request):
    return {"status": "API is healthy."}


@router.get("/jweifjwiefj", status_code=200)
def jweifjwiefj(request: Request):
    return {"jweifjwiefj": "huehuehuehuehue"}

@router.get("/analytics")
def get_analytics(request: Request, auth_user_controller: AuthUserController = Depends(get_auth_user_controller), guardian_controller: GuardianController = Depends(get_guardian_controller), outpass_controller: OutpassController = Depends(get_outpass_controller)):
    students = auth_user_controller.get_students()
    wardens = auth_user_controller.get_wardens()
    guardians = guardian_controller.get_multi()
    unverified_guardians = sum(1 for guardian in guardians if not guardian.is_verified)
    outpasses = outpass_controller.get_multi()


    return {
        "students": len(students),
        "wardens": len(wardens),
        "unverified guardians": unverified_guardians,
        "outpasses": len(outpasses),
    }
