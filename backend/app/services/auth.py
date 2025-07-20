# Update your backend/app/services/auth.py with debug logging

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import hash_password, verify_password, create_access_token


def create_user(db: Session, user_in: UserCreate) -> User:
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ DEBUG: Created user with ID: {user.id}, email: {user.email}")
    return user


def authenticate(db: Session, email: str, password: str) -> tuple[str, User]:
    user = db.query(User).filter(User.email == email).first()
    print(f"🔍 DEBUG: Looking for user with email: {email}")
    
    if not user:
        print("❌ DEBUG: User not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    print(f"🔍 DEBUG: Found user: ID={user.id}, email={user.email}, active={user.is_active}")
    
    if not verify_password(password, user.hashed_password):
        print("❌ DEBUG: Password verification failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    print("✅ DEBUG: Password verified successfully")
    
    # Create token with user ID as 'sub'
    token_data = {"sub": user.id}
    print(f"🔍 DEBUG: Creating token with data: {token_data}")
    
    token = create_access_token(token_data)
    print(f"🔍 DEBUG: Created token: {token}")
    
    return token, user
