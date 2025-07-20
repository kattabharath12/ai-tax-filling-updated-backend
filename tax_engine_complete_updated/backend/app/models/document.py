from sqlalchemy import Column, Integer, String, Enum, BigInteger, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
import enum

from ..core.db import Base


class DocumentType(enum.Enum):
    w2 = "w2"
    form_1099 = "1099"
    receipt = "receipt"
    bank_statement = "bank_statement"
    other = "other"


class DocumentStatus(enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    processed = "processed"
    error = "error"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    document_type = Column(Enum(DocumentType), default=DocumentType.other)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.uploaded)
    extracted_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    owner = relationship("User", backref="documents")