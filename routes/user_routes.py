from fastapi import APIRouter, Depends, HTTPException, Header
from models import Cliente, Endereco
from assets.hash import bcrypt_context
from schemas import CadastrarCliente, Login, EditarCliente, CriarEndereco, EditarEndereco, DeletarEndereco, ListarEnderecos
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


@user_router.post("/user/criar_endereco")
async def criar_endereco(request: CriarEndereco, session: Session = Depends(get_session), token: str = Header(...)):
    token_decodificado = decodificar_token(token)

    sub = token_decodificado.get("sub")
    exp = token_decodificado.get("exp")

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Token expirado")
    try:
        id_cliente = UUID(sub)
    except Exception as e:
         logger.error(f"Erro ao gerar UUID: {e}")
         raise HTTPException(status_code=400, detail="ID inválido")
    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    endereco = Endereco(cliente_id=cliente.id, 
                        endereco=request.endereco, 
                        complemento=request.complemento, 
                        bairro=request.bairro, 
                        cidade=request.cidade, 
                        estado=request.estado, 
                        cep=request.cep, 
                        referencia=request.ref)
    

    try:
            session.add(endereco)
            session.commit()
            return {"mensagem": "Endereço criado com sucesso!"}
    except Exception as e:
            session.rollback()
            logger.error(f"Erro ao criar endereço: {e}")
            raise HTTPException(status_code=500, detail="Erro ao criar endereço")


@user_router.put("/user/editar_endereco/")
async def editar_endereco(request: EditarEndereco, session: Session = Depends(get_session), token: str = Header(...)):

    token_decodificado = decodificar_token(token)

    sub = token_decodificado.get("sub")
    exp = token_decodificado.get("exp")

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Token expirado")

    id_cliente = UUID(sub)

    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")       

    endereco = session.query(Endereco).filter(Endereco.cliente_id == cliente.id).first()
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado para este cliente")
    
    if request.endereco is not None:
            endereco.endereco = request.endereco
    if request.complemento is not None:
            endereco.complemento = request.complemento
    if request.referencia is not None:
            endereco.referencia = request.referencia
    if request.bairro is not None:
            endereco.bairro = request.bairro
    if request.cidade is not None:
            endereco.cidade = request.cidade
    if request.estado is not None:
            endereco.estado = request.estado
    if request.cep is not None:
            endereco.cep = request.cep
    try:
        session.commit()
        return {"mensagem": "Endereço atualizado com sucesso!", "endereco": endereco}
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao atualizar endereço: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar endereço")
    
@user_router.delete("/user/deletar_endereco/")
async def deletar_endereco(request: DeletarEndereco, session: Session = Depends(get_session), token: str = Header(...)):

    token_decodificado = decodificar_token(token)

    sub = token_decodificado.get("sub")
    exp = token_decodificado.get("exp")

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Token expirado")

    id_cliente = UUID(sub)

    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")       

    endereco = session.query(Endereco).filter(Endereco.id == request.endereco_id, Endereco.cliente_id == cliente.id).first()
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado para este cliente")     
    
    try:
        session.delete(endereco)
        session.commit()
        return {"mensagem": "Endereço deletado com sucesso!"}
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao deletar endereço: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar endereço")

@user_router.get("/user/listar_enderecos/")
async def listar_enderecos(session: Session = Depends(get_session), token: str = Header(...)):
    
    token_decodificado = decodificar_token(token)

    sub = token_decodificado.get("sub")
    exp = token_decodificado.get("exp")

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Token expirado")
    try:
            id_cliente = UUID(sub)
    except Exception as e:
            logger.error(f"Erro ao gerar UUID: {e}")
            raise HTTPException(status_code=400, detail="ID inválido")
    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()

    if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")      

    enderecos = session.query(Endereco).filter(Endereco.cliente_id == cliente.id).all()
    if not enderecos:
        raise HTTPException(status_code=404, detail="Endereço não encontrado para este cliente")
    
    return {
         "enderecos": [{
              "id": endereco.id,
              "endereco": endereco.endereco,
              "bairro": endereco.bairro,
              "cidade": endereco.cidade,
              "estado": endereco.estado
         }for endereco in enderecos]
    }

@user_router.post("/user/mostrar_endereco/")
async def mostrar_endereco(request: ListarEnderecos, session: Session = Depends(get_session), token: str = Header(...)):

    token_decodificado = decodificar_token(token)

    sub = token_decodificado.get("sub")
    exp = token_decodificado.get("exp")

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Token expirado")

    id_cliente = UUID(sub)

    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    endereco = session.query(Endereco).filter(Endereco.id == request.id_endereco, Endereco.cliente_id == cliente.id).first()
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado para este cliente")

    return {"mensagem": "Endereço encontrado com sucesso!", "endereco": endereco}