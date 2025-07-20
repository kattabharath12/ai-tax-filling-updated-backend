from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..core.dependencies import get_db, get_current_user
from ..schemas.document import DocumentRead
from ..services import documents as doc_service
from ..models.user import User

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=List[DocumentRead], status_code=201)
async def upload_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    return doc_service.upload_documents(db, current_user.id, files)


@router.get("/", response_model=List[DocumentRead])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return doc_service.get_user_documents(db, current_user.id)