from sqlalchemy import Column, Integer, String, Enum, JSON, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
import enum

from ..core.db import Base


class FormStatus(enum.Enum):
    draft = "draft"
    in_progress = "in_progress"
    completed = "completed"
    filed = "filed"


class TaxForm(Base):
    __tablename__ = "tax_forms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    form_type = Column(String(50), nullable=False)
    tax_year = Column(Integer, nullable=False)
    status = Column(Enum(FormStatus), default=FormStatus.draft)
    form_data = Column(JSON)
    calculated_tax = Column(DECIMAL(10, 2))
    refund_amount = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    owner = relationship("User", backref="forms")