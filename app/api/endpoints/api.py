from fastapi import APIRouter

from .auth_users import router as auth_user_router
from .guardians import router as guardian_router
from .logs import router as logs_router
from .outpass import router as outpass_router

router = APIRouter()
router.include_router(logs_router)
router.include_router(auth_user_router)
router.include_router(guardian_router)
router.include_router(outpass_router)
