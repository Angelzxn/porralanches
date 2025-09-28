import re

def limpar_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)