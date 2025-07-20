# Update your backend/app/core/dependencies.py - Handle string user ID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .db import SessionLocal
from .security import decode_token
from ..models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    print(f"🔍 DEBUG: Received token: {token}")
    
    try:
        payload = decode_token(token)
        print(f"🔍 DEBUG: Decoded payload: {payload}")
        
        user_id_str: str = payload.get("sub")
        print(f"🔍 DEBUG: Extracted user_id (string): {user_id_str}")
        
        if user_id_str is None:
            print("❌ DEBUG: user_id is None")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials - no sub in payload")
        
        # FIX: Convert string back to integer for database lookup
        try:
            user_id = int(user_id_str)
            print(f"🔍 DEBUG: Converted to user_id (int): {user_id}")
        except ValueError:
            print(f"❌ DEBUG: Could not convert user_id to int: {user_id_str}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format")
            
    except ValueError as e:
        print(f"❌ DEBUG: Token decode error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials - token decode failed")

    user = db.query(User).filter(User.id == user_id).first()
    print(f"🔍 DEBUG: Found user: {user}")
    print(f"🔍 DEBUG: User active: {user.is_active if user else 'No user found'}")
    
    if not user or not user.is_active:
        print("❌ DEBUG: User not found or inactive")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    
    print(f"✅ DEBUG: Returning user: {user.email}")
    return user
