from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from marketlab.infra.auth.jwt import create_access_token
from marketlab.infra.auth.passwords import hash_password, verify_password
from marketlab.infra.db.models import UserRow
from marketlab.infra.db.repos.user_repo import UserRepo
from marketlab.infra.db.session import get_db
from marketlab.api.deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])



class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    token: str
    user_id: str
    email: str

class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=128)

class MessageOut(BaseModel):
    message: str


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    repo = UserRepo(db)

    if repo.get_by_email(body.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = UserRow(
        email=body.email,
        password_hash=hash_password(body.password),
    )
    repo.create(user)
    db.commit()

    token = create_access_token(user.id)
    return TokenOut(token=token, user_id=user.id, email=user.email)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    repo = UserRepo(db)
    user = repo.get_by_email(body.email)

    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
        )

    token = create_access_token(user.id)
    return TokenOut(token=token, user_id=user.id, email=user.email)


@router.post("/change-password", response_model=MessageOut)
def change_password(
    body: ChangePasswordIn,
    current_user: UserRow = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(body.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    current_user.password_hash = hash_password(body.new_password)
    db.commit()
    return MessageOut(message="Password changed successfully")


@router.get("/me", response_model=TokenOut)
def get_me(current_user: UserRow = Depends(get_current_user)):
    return TokenOut(
        token="",
        user_id=current_user.id,
        email=current_user.email,
    )
