from pathlib import Path
import shutil
from typing import Sequence
from sqlalchemy.orm import Session
from fastapi import UploadFile
import uuid

from ..core.config import get_settings
from ..models.document import Document, DocumentStatus, DocumentType

settings = get_settings()


def save_upload_file(file: UploadFile, destination: Path) -> Path:
    """Stream-copy the uploaded file to destination"""
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return destination


def upload_documents(
    db: Session,
    user_id: int,
    files: Sequence[UploadFile],
    doc_type: str | None = None,
) -> list[Document]:
    saved_docs = []
    settings.upload_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        if file.size and file.size > settings.max_file_size:
            continue  # skip oversized

        # Generate unique filename
        file_extension = Path(file.filename).suffix if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        dest = settings.upload_dir / unique_filename

        save_upload_file(file, dest)

        doc = Document(
            user_id=user_id,
            filename=file.filename or unique_filename,
            file_path=str(dest),
            file_type=file.content_type or "application/octet-stream",
            file_size=dest.stat().st_size,
            document_type=DocumentType(doc_type) if doc_type else DocumentType.other,
            status=DocumentStatus.uploaded,
        )
        db.add(doc)
        saved_docs.append(doc)

    db.commit()
    for d in saved_docs:
        db.refresh(d)
    return saved_docs


def get_user_documents(db: Session, user_id: int) -> list[Document]:
    return db.query(Document).filter(Document.user_id == user_id).all()