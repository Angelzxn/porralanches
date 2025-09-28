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

class CadastrarEmpresa(BaseModel):
    titulo: str
    razao_social: str
    cnpj: str
    senha: str
    
    class Config:
        from_attributes = True