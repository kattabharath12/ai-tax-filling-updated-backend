# Update your backend/app/core/security.py with debug logging

from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def create_access_token(data: dict[str, Any], expires_delta: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    
    print(f"🔍 DEBUG: Creating token with payload: {to_encode}")
    print(f"🔍 DEBUG: Using SECRET_KEY: {settings.secret_key[:10]}... (truncated)")
    print(f"🔍 DEBUG: Using ALGORITHM: {settings.algorithm}")
    
    encoded_token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    print(f"🔍 DEBUG: Encoded token: {encoded_token}")
    
    return encoded_token


def decode_token(token: str) -> dict[str, Any]:
    try:
        print(f"🔍 DEBUG: Attempting to decode token: {token}")
        print(f"🔍 DEBUG: Using SECRET_KEY: {settings.secret_key[:10]}... (truncated)")
        print(f"🔍 DEBUG: Using ALGORITHM: {settings.algorithm}")
        
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print(f"✅ DEBUG: Successfully decoded payload: {payload}")
        return payload
        
    except JWTError as err:
        print(f"❌ DEBUG: JWT decode error: {err}")
        print(f"❌ DEBUG: Error type: {type(err)}")
        raise ValueError("Invalid credentials") from err
    except Exception as err:
        print(f"❌ DEBUG: Unexpected error: {err}")
        print(f"❌ DEBUG: Error type: {type(err)}")
        raise ValueError("Invalid credentials") from err
