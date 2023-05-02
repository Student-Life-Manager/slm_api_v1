"""
Authuser endpoint
"""

from fastapi import APIRouter

from .main import router as main_router
from .students import router as student_router
from .warden import router as warden_router

router = APIRouter()

router.include_router(main_router, tags=["auth_user"])
router.include_router(student_router, tags=["student"])
router.include_router(warden_router, tags=["warden"])
