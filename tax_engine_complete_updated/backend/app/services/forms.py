from sqlalchemy.orm import Session
from typing import Any

from ..models.tax_form import TaxForm, FormStatus
from ..schemas.tax_form import TaxFormCreate, TaxFormUpdate


def list_forms(db: Session, user_id: int) -> list[TaxForm]:
    return db.query(TaxForm).filter(TaxForm.user_id == user_id).all()


def create_form(db: Session, user_id: int, form_in: TaxFormCreate) -> TaxForm:
    form = TaxForm(
        user_id=user_id, 
        form_type=form_in.form_type, 
        tax_year=form_in.tax_year, 
        status=FormStatus.draft
    )
    db.add(form)
    db.commit()
    db.refresh(form)
    return form


def update_form(db: Session, form_id: int, user_id: int, form_update: TaxFormUpdate) -> TaxForm:
    form = db.query(TaxForm).filter(TaxForm.id == form_id, TaxForm.user_id == user_id).first()
    if not form:
        raise ValueError("Form not found")

    form.form_data = form_update.form_data
    form.status = FormStatus.in_progress
    db.commit()
    db.refresh(form)
    return form


def get_form(db: Session, form_id: int, user_id: int) -> TaxForm:
    form = db.query(TaxForm).filter(TaxForm.id == form_id, TaxForm.user_id == user_id).first()
    if not form:
        raise ValueError("Form not found")
    return form