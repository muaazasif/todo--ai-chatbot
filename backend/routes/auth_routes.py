from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from auth import UserCreate, UserLogin, Token, create_access_token, verify_password, get_password_hash
from models import User, engine
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import verify_token, TokenData
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/register", response_model=Token)
def register(user: UserCreate):
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        existing_email = session.exec(select(User).where(User.email == user.email)).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=get_password_hash(user.password)
        )
        session.add(db_user)
        try:
            session.commit()
            session.refresh(db_user)
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_ERROR,
                detail=f"Registration failed: {str(e)}"
            )

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    with Session(engine) as session:
        try:
            # Find user by username
            user = session.exec(select(User).where(User.username == credentials.username)).first()

            if not user or not verify_password(credentials.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Create access token
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                data={"sub": credentials.username}, expires_delta=access_token_expires
            )

            return {"access_token": access_token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_ERROR,
                detail=f"Login failed: {str(e)}"
            )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token_data = verify_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == token_data.username)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user