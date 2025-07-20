from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.dependencies import get_db, get_current_user
from ..schemas.payment import PaymentRead, PaymentCreate
from ..services import payments as pay_service
from ..models.user import User

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.get("/", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return pay_service.list_payments(db, current_user.id)


@router.post("/", response_model=PaymentRead, status_code=201)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return pay_service.create_payment(db, current_user.id, payment_in)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return pay_service.get_payment(db, payment_id, current_user.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Payment not found")