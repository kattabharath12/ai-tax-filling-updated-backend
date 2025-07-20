from pydantic import BaseModel
from typing import Any
from datetime import datetime


class TaxFormRead(BaseModel):
    id: int
    form_type: str
    tax_year: int
    status: str
    form_data: dict[str, Any] | None = None
    calculated_tax: float | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class TaxFormCreate(BaseModel):
    form_type: str
    tax_year: int


class TaxFormUpdate(BaseModel):
    form_data: dict[str, Any]