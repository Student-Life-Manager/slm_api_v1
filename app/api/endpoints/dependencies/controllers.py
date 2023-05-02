"""
controller dependency injection
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers import AuthUserController, GuardianController, OutpassController
from app.crud import CRUDAuthUser, CRUDGuardian, CRUDOutpass
from app.database.session import get_db
from app.models import AuthUser, Guardian, Outpass


def get_auth_user_controller(db: Session = Depends(get_db)):
    """
    dependency controller for loading AuthUserController
    """
    crud_auth_user = CRUDAuthUser(db=db, model=AuthUser)

    return AuthUserController(db=db, crud_auth_user=crud_auth_user)


def get_guardian_controller(db: Session = Depends(get_db)):
    """
    dependency controller for loading GuardianController
    """
    crud_guardian = CRUDGuardian(db=db, model=Guardian)

    return GuardianController(db=db, crud_guardian=crud_guardian)


def get_outpass_controller(db: Session = Depends(get_db)):
    """
    dependency controller for loading OutpassController
    """
    crud_outpass = CRUDOutpass(db=db, model=Outpass)

    return OutpassController(db=db, crud_outpass=crud_outpass)
