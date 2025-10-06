from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

# Usuário (tabela de login / controle de acesso)
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    is_admin: bool = False

# Departamento (ex: RH, Financeiro, Logística)
class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

# Funcionário (ligação entre usuário e departamento)
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    role: Optional[str] = None
    hire_date: date = Field(default_factory=lambda: date.today())

# Solicitação de férias/licença
class Leave(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: str = Field(default="pending")  # pending | approved | rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
