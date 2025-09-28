from fastapi import APIRouter, Depends, HTTPException, Header
from models import Cliente
from assets.hash import bcrypt_context
from schemas import CadastrarCliente, Login, EditarCliente
from sqlalchemy.orm import Session
from sqlalchemy import or_
from assets.dependecies import get_session
from assets.formatacoes import limpar_cpf
from assets.validacoes import validar_cpf, validar_email, validar_senha
from assets.token import criar_token, decodificar_token
import logging
from uuid import UUID
from datetime import datetime, timezone
from assets.hash import bcrypt_context

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.put("/edit_info/")
async def edit_info(request: EditarCliente, session: Session = Depends(get_session), token: str = Header(...)):

    token_decodificado = decodificar_token(token)

    sub = token_decodificado.get("sub")
    exp = token_decodificado.get("exp")

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Token expirado")

    id_cliente = UUID(sub)

    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()

    

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if request.nome_completo is not None:
        cliente.nome_completo = request.nome_completo
        
    if request.email is not None:
        if not validar_email(request.email):
            raise HTTPException(status_code=400, detail="E-mail inválido")
        cliente.email = request.email

    if request.cpf is not None:
        if not validar_cpf(limpar_cpf(request.cpf)):
            raise HTTPException(status_code=400, detail="CPF inválido")
        cliente.cpf = request.cpf

    if request.senha is not None:
        if not validar_senha(request.senha):
            raise HTTPException(status_code=400, detail="Sua senha não segue nossas regras")
        senha_hash = bcrypt_context.hash(request.senha[:72])
        cliente.senha = senha_hash
    
    try:
        session.commit()

    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao atualizar informações do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar informações do cliente")


    return {"mensagem": "Informações atualizadas com sucesso!"}