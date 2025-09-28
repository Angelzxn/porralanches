import re

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica tamanho e casos repetidos óbvios
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Função para calcular cada dígito verificador
    def calcular_digito(cpf_parcial):
        soma = sum(int(num) * peso for num, peso in zip(cpf_parcial, range(len(cpf_parcial)+1, 1, -1)))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    # Calcula os dois dígitos
    digito1 = calcular_digito(cpf[:9])
    digito2 = calcular_digito(cpf[:9] + str(digito1))

    # Verifica se bate com os dígitos do CPF
    return cpf[-2:] == f"{digito1}{digito2}"

def validar_email(email: str) -> bool:
    # Regex pra validar e-mail
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None
