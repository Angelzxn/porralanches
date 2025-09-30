from pydantic import BaseModel
from typing import Optional

class CadastrarCliente(BaseModel):
    nome_completo: str
    email: str
    cpf: str
    senha: str

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: Optional[str]
    cpf: Optional[str]
    senha: str

    class Config:
        from_attributes = True


class EditarCliente(BaseModel):
    nome_completo: Optional[str]
    email: Optional[str]
    cpf: Optional[str]
    senha: Optional[str]

class CadastrarEmpresa(BaseModel):
    titulo: str
    razao_social: str
    cnpj: str
    senha: str
    
    class Config:
        from_attributes = True

class LoginEmpresa(BaseModel):
    cnpj: str
    senha: str

    class Config:
        from_attributes = True

class CriarEndereco(BaseModel):
    rua: str
    numero: str
    complemento: Optional[str]
    bairro: str
    cidade: str
    estado: str
    cep: str

    class Config:
        from_attributes = True

class EditarEndereco(BaseModel):
    endereco: Optional[str]
    complemento: Optional[str]
    referencia: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    cep: Optional[str]

    class Config:
        from_attributes = True

class DeletarEndereco(BaseModel):
    endereco_id: int

    class Config:
        from_attributes = True

class ListarEnderecos(BaseModel):
    id: Optional[int]
    id_cliente: int
    class Config:
        from_attributes = True