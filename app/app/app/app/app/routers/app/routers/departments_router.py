from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Department
from ..schemas import DepartmentCreate, DepartmentRead
from ..deps import admin_required

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=DepartmentRead, dependencies=[Depends(admin_required)])
def create_department(payload: DepartmentCreate, session: Session = Depends(get_session)):
    # evita nomes duplicados
    exists = session.exec(select(Department).where(Department.name == payload.name)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Department already exists")
    d = Department(name=payload.name)
    session.add(d)
    session.commit()
    session.refresh(d)
    return d

@router.get("/", response_model=list[DepartmentRead])
def list_departments(session: Session = Depends(get_session)):
    return session.exec(select(Department)).all()
