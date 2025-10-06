from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..models import Employee, User, Department
from ..schemas import EmployeeCreate, EmployeeRead
from ..deps import admin_required

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeRead, dependencies=[Depends(admin_required)])
def create_employee(payload: EmployeeCreate, session: Session = Depends(get_session)):
    # valida usuário e departamento
    if not session.get(User, payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not session.get(Department, payload.department_id):
        raise HTTPException(status_code=404, detail="Department not found")

    emp = Employee(**payload.model_dump())
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@router.get("/", response_model=list[EmployeeRead])
def list_employees(session: Session = Depends(get_session)):
    return session.query(Employee).all()
