import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth_router, employees_router, departments_router, leaves_router

# Inicializa o banco de dados
init_db()

# Cria a aplicação FastAPI
app = FastAPI(title="RH System")

# Configuração de CORS (libera requisições externas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importa e inclui as rotas
app.include_router(auth_router.router)
app.include_router(departments_router.router)
app.include_router(employees_router.router)
app.include_router(leaves_router.router)

# Endpoint raiz (teste rápido)
@app.get("/")
def root():
    return {"status": "ok", "service": "RH System"}
