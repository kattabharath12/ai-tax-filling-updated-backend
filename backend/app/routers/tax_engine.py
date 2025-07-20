from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..core.dependencies import get_db, get_current_user
from ..services.tax_engine import calculate_tax, calculate_quarterly_payments, validate_tax_form_data
from ..models.user import User

router = APIRouter(prefix="/api/tax-engine", tags=["tax-engine"])


class TaxCalculationRequest(BaseModel):
    income: float = Field(..., ge=0, description="Annual gross income")
    deductions: float = Field(0, ge=0, description="Total deductions")
    filing_status: str = Field("single", description="Filing status")


class QuarterlyPaymentRequest(BaseModel):
    annual_tax: float = Field(..., ge=0, description="Annual tax liability")


class FormValidationRequest(BaseModel):
    form_data: Dict[str, Any] = Field(..., description="Tax form data to validate")


@router.post("/calculate")
def calculate_taxes(
    request: TaxCalculationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Calculate tax liability based on income and deductions"""
    result = calculate_tax(
        income=request.income,
        deductions=request.deductions,
        filing_status=request.filing_status
    )
    return result


@router.post("/quarterly-payments")
def get_quarterly_payments(
    request: QuarterlyPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Calculate quarterly estimated tax payments"""
    return calculate_quarterly_payments(request.annual_tax)


@router.post("/validate-form")
def validate_form(
    request: FormValidationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Validate tax form data for errors and warnings"""
    return validate_tax_form_data(request.form_data)