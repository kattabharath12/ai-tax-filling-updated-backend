from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class DocumentType(str, Enum):
    w2 = "w2"
    form_1099 = "1099"
    receipt = "receipt"
    bank_statement = "bank_statement"
    other = "other"


class DocumentRead(BaseModel):
    id: int
    filename: str
    document_type: DocumentType
    status: str
    created_at: datetime

    class Config:
        from_attributes = True