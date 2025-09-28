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

<<<<<<< HEAD
class EditarCliente(BaseModel):
    nome_completo: Optional[str]
    email: Optional[str]
    cpf: Optional[str]
    senha: Optional[str]
=======
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
>>>>>>> 2ae0b9a97f14975ae6decfb939893d1249e6f3a8

    class Config:
        from_attributes = True