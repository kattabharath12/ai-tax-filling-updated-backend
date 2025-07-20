from sqlalchemy.orm import Session
from ..models.payment import Payment, PaymentStatus, PaymentType
from ..schemas.payment import PaymentCreate
import uuid


def list_payments(db: Session, user_id: int) -> list[Payment]:
    return db.query(Payment).filter(Payment.user_id == user_id).all()


def create_payment(db: Session, user_id: int, payment_in: PaymentCreate) -> Payment:
    payment = Payment(
        user_id=user_id,
        form_id=payment_in.form_id,
        payment_type=PaymentType(payment_in.payment_type),
        amount=payment_in.amount,
        status=PaymentStatus.pending,
        reference_number=f"PAY-{uuid.uuid4().hex[:8].upper()}",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int, user_id: int) -> Payment:
    payment = db.query(Payment).filter(Payment.id == payment_id, Payment.user_id == user_id).first()
    if not payment:
        raise ValueError("Payment not found")
    return payment