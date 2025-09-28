from pydantic import BaseModel

class CadastrarCliente(BaseModel):
    nome_completo: str
    email: str
    cpf: str
    senha: str

    class Config:
        from_attributes = True