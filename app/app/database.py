from sqlmodel import SQLModel, create_engine, Session
import os

# Caminho do banco de dados (SQLite por padrão)
DB_URL = os.getenv("DB_URL", "sqlite:///./rhsystem.db")

# Ajuste necessário para SQLite (para permitir múltiplas conexões)
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

# Cria o engine do banco
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)

# Inicializa o banco de dados (cria as tabelas)
def init_db() -> None:
    SQLModel.metadata.create_all(engine)

# Retorna uma sessão de banco
def get_session():
    with Session(engine) as session:
        yield session
