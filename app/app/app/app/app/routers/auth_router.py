from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import User
from ..schemas import Token, LoginRequest, RegisterRequest
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    # Verifica se já existe usuário com esse e-mail
    if session.exec(select(User).where(User.email == data.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    # Cria usuário
    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        is_admin=data.is_admin,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    # Gera token
    token = create_access_token({"sub": str(user.id), "email": user.email, "admin": user.is_admin})
    return Token(access_token=token)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email, "admin": user.is_admin})
    return Token(access_token=token)
