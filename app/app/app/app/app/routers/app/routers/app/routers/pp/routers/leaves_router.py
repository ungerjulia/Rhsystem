from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Leave, Employee
from ..schemas import LeaveCreate, LeaveRead
from ..deps import get_current_user, admin_required

router = APIRouter(prefix="/leaves", tags=["leaves"])

# Solicitação de férias/licença
@router.post("/", response_model=LeaveRead)
def request_leave(
    payload: LeaveCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    emp = session.get(Employee, payload.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    leave = Leave(**payload.model_dump())
    session.add(leave)
    session.commit()
    session.refresh(leave)
    return leave

# Aprovar solicitação (somente admin)
@router.post("/{leave_id}/approve", dependencies=[Depends(admin_required)])
def approve_leave(leave_id: int, session: Session = Depends(get_session)):
    leave = session.get(Leave, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.status = "approved"
    session.add(leave)
    session.commit()
    return {"ok": True, "message": "Leave approved"}

# Rejeitar solicitação (somente admin)
@router.post("/{leave_id}/reject", dependencies=[Depends(admin_required)])
def reject_leave(leave_id: int, session: Session = Depends(get_session)):
    leave = session.get(Leave, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.status = "rejected"
    session.add(leave)
    session.commit()
    return {"ok": True, "message": "Leave rejected"}

# Listar todas as solicitações
@router.get("/", response_model=list[LeaveRead])
def list_leaves(session: Session = Depends(get_session)):
    return session.exec(select(Leave)).all()
