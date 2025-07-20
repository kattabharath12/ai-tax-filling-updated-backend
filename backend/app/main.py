from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .core.config import get_settings
from .core.db import Base, engine
from .routers import auth, documents, forms, payments, tax_engine

settings = get_settings()

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)

# Create DB tables (for dev only; use Alembic migrations in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tax Engine API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(forms.router)
app.include_router(payments.router)
app.include_router(tax_engine.router)


@app.get("/health")
def health():
    return {"status": "ok"}

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway sets PORT automatically
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
