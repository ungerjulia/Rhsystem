from datetime import date
from typing import Optional
from pydantic import BaseModel

# --- Autenticação ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    full_name: str
    password: str
    is_admin: bool = False

# --- Departamentos ---
class DepartmentCreate(BaseModel):
    name: str

class DepartmentRead(BaseModel):
    id: int
    name: str

# --- Funcionários ---
class EmployeeCreate(BaseModel):
    user_id: int
    department_id: int
    role: Optional[str] = None

class EmployeeRead(BaseModel):
    id: int
    user_id: int
    department_id: int
    role: Optional[str]

# --- Férias / Licenças ---
class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveRead(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str]
    status: str
