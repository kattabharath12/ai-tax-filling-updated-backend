from pydantic import BaseModel
from datetime import datetime


class PaymentRead(BaseModel):
    id: int
    payment_type: str
    amount: float
    status: str
    reference_number: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    form_id: int | None = None
    payment_type: str
    amount: float