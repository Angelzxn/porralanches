from fastapi import APIRouter, Depends, HTTPException
from models import Cliente
from assets.hash import bcrypt_context
from schemas import CadastrarCliente
from sqlalchemy.orm import Session
from assets.dependecies import get_session

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

auth_router.post("/cliente/cadastro")
async def cadastrar_cliente(request: CadastrarCliente, session: Session = Depends(get_session)):
    