from fastapi import APIRouter, Depends, HTTPException, Header
from models import Cliente
from assets.hash import bcrypt_context
from schemas import CadastrarCliente, Login, CadastrarEmpresa
from sqlalchemy.orm import Session
from sqlalchemy import or_
from assets.dependecies import get_session
from assets.formatacoes import limpar_cpf
from assets.validacoes import validar_cpf, validar_email, validar_senha
from assets.token import criar_token
import logging

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------------------------- Cliente --------------------------------------------------------------- #

auth_router.post("/cliente/cadastro")
async def cadastrar_cliente(request: CadastrarCliente, session: Session = Depends(get_session)):
    if not validar_cpf(limpar_cpf(request.cpf)):
        raise HTTPException(status_code=400, detail="CPF inválido!")
    
    if not validar_email(email=request.email):
        raise HTTPException(status_code=400, detail="E-mail inválido!")
    
    if not validar_senha(request.senha):
        raise HTTPException(status_code=400, detail="Sua senha não segue nossas regras")
    
    ja_existe = session.query(Cliente).filter(or_(Cliente.cpf == limpar_cpf(request.cpf),
                                                  Cliente.email == request.email)).first()
    if ja_existe:
        raise HTTPException(status_code=409, detail="Já existe um cliente com esse e-mail ou senha")
    
    senha = bcrypt_context.hash(request.senha[:72])
    new = Cliente(nome=request.nome.title(), 
                  email=request.email, 
                  cpf=limpar_cpf(request.cpf), 
                  senha=senha)
    
    try:
        session.add(new)
        session.commit()
        return {
            "mensagem": "Cadastro realizado!",
            "nome": new.nome_completo,
            "access-token": criar_token(new.id),
            "token-type": "Bearer"
        }
    except Exception as e:
        logger.error(f"Erro ao cadastrar usuário: {e}")
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente")
    


auth_router.post("/cliente/login")
async def login_cliente(request: Login, session: Session = Depends(get_session)):
    cpf = "a" if not request.cpf else request.cpf
    email = "a" if not request.email else request.email
    
    user = session.query(Cliente).filter(or_(Cliente.cpf == cpf, Cliente.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    correta = bcrypt_context.verify(request.senha, user.senha)
    if not correta:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    if not user.ativo:
        raise HTTPException(status_code=403, detail="Usuário inativo")

    return {
        "nome": user.nome_completo,
        "access-token": criar_token(user.id),
        "token-type": "Bearer"
    }


# ------------------------------- Empresa ---------------------------------------------------------- #
auth_router.post("/empresa/cadastro")
async def cadastrar_empresa(request: CadastrarEmpresa, session: Session = Depends(get_session)):
    