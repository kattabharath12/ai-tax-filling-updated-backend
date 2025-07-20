from sqlalchemy import Column, Integer, String, Enum, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
import enum

from ..core.db import Base


class PaymentStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class PaymentType(enum.Enum):
    tax_payment = "tax_payment"
    refund = "refund"
    penalty = "penalty"
    interest = "interest"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    form_id = Column(Integer, ForeignKey("tax_forms.id"))
    payment_type = Column(Enum(PaymentType), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    reference_number = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", backref="payments")