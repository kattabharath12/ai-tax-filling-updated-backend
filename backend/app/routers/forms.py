from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.dependencies import get_db, get_current_user
from ..schemas.tax_form import TaxFormRead, TaxFormCreate, TaxFormUpdate
from ..services import forms as form_service
from ..models.user import User

router = APIRouter(prefix="/api/forms", tags=["forms"])


@router.get("/", response_model=list[TaxFormRead])
def list_forms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return form_service.list_forms(db, current_user.id)


@router.post("/", response_model=TaxFormRead, status_code=201)
def create_form(
    form_in: TaxFormCreate,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return form_service.create_form(db, current_user.id, form_in)


@router.get("/{form_id}", response_model=TaxFormRead)
def get_form(
    form_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return form_service.get_form(db, form_id, current_user.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Form not found")


@router.put("/{form_id}", response_model=TaxFormRead)
def update_form(
    form_id: int,
    form_update: TaxFormUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return form_service.update_form(db, form_id, current_user.id, form_update)
    except ValueError:
        raise HTTPException(status_code=404, detail="Form not found")