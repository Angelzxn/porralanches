import re

def limpar_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)

def formatar_cnpj(cnpj: str, apenas_numeros=False) -> str:
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if apenas_numeros:
        return cnpj
    if len(cnpj) != 14:
        return cnpj  # retorna como está se não tiver 14 dígitos
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"