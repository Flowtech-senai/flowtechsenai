import re
import requests

class Validator:
    TOKEN_INVERTEXTO = "22461|EHBKg1qLsqcDVFphzHYHXAU0ilV1KMMe" # meu token do invertexto
    
    @staticmethod
    def required(value, field_name):
        if value is None or str(value).strip() == "":
            return f"O campo {field_name} é obrigatório." # campo obrigatório de ser preenchido
        return None

    @staticmethod
    def non_negative(value, field_name): # o valor desse campo nao pode ser negativo (menor que zero)
        try:
            if float(value) < 0:
                return f"O campo {field_name} não pode ser negativo."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico." # o valor do campo precissa ser um número (não letra)
        return None

    @staticmethod
    def positive(value, field_name): # apenas número positivo
        try:
            if int(value) <= 0: # se o valor for menor ou igual a zero mostra uma mensagem.
                return f"O campo {field_name} deve ser maior que zero."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None

    @staticmethod
    def validar_email_estrutura(email: str) -> bool: # validação de email
        # Retorna True se o e-mail tiver uma estrutura real aceitável.
        padrao = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(padrao, email))

    @staticmethod
    def validar_cnpj_real(cnpj: str) -> bool: # validação de cnpj (apenas cnpj verdadeiro)
        numeros = re.sub(r'\D', '', str(cnpj))
        if len(numeros) != 14 or len(set(numeros)) == 1: # se a quantidade total for diferente que 14 está errado
            return False

        def calcular_digito(cnpj_parcial, pesos):
            soma = sum(int(num) * peso for num, peso in zip(cnpj_parcial, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        pesos_v1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos_v2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        if calcular_digito(numeros[:12], pesos_v1) != int(numeros[12]):
            return False
        if calcular_digito(numeros[:13], pesos_v2) != int(numeros[13]):
            return False

        return True
    
    @staticmethod
    def validar_email_externo_real(email: str) -> bool:
        # Validação local, se tem a estrutura com @ e ponto depois
        if not email:
            return False
        return Validator.validar_email_estrutura(email)


    @staticmethod
    def validar_telefone_externo_br(telefone: str) -> bool: # Usa a API do Invertexto para validar a estrutura do telefone, checando se o DDD é real, se o tamanho é oficial e se a operadora é válida.
      
        tel_limpo = re.sub(r'\D', '', str(telefone))
        if not tel_limpo:
            return False
            
        url = "https://invertexto.com"
        params = {
            "token": Validator.TOKEN_INVERTEXTO,
            "value": tel_limpo
        }
        
        try:
            resposta = requests.get(url, params=params, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados.get("valid", False)
            return False
        except requests.RequestException:
            # se a API cair, aceita se tiver 11 números
            return len(tel_limpo) == 11

    TOKEN2= "22841|aYmRF9pt8ipmwXUVa3vIXy3FkNsXIRcD"

    @staticmethod
    def validar_cnpj_externo_receita(cnpj: str) -> bool: # Consulta o CNPJ no Invertexto para validar se ele existe na Receita Federal

        cnpj_limpo = re.sub(r'\D', '', str(cnpj))
        if len(cnpj_limpo) != 14:
            return False
            
        url = "https://invertexto.com"
        params = {
            "token": Validator.TOKEN2,
            "cnpj": cnpj_limpo
        }
        
        try:
            resposta = requests.get(url, params=params, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados.get("situacao_cadastral") == "ATIVA"
            return False
        except requests.RequestException:
            return Validator.validar_cnpj_real(cnpj_limpo)

    @staticmethod
    def validar_cpf_real(cpf: str) -> bool:
        """Valida o CPF usando o cálculo oficial de dígitos verificadores."""
        numeros = re.sub(r'\D', '', str(cpf))
        if len(numeros) != 11 or len(set(numeros)) == 1:
            return False

        # Cálculo do primeiro dígito
        soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        d1 = 0 if resto < 2 else 11 - resto
        if int(numeros[9]) != d1:
            return False

        # Cálculo do segundo dígito
        soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        d2 = 0 if resto < 2 else 11 - resto
        return int(numeros[10]) == d2

    @staticmethod
    def validar_maioridade(data_nascimento) -> bool:
        """Garante que a data de nascimento resulte em pelo menos 18 anos (maior de 17)."""
        from datetime import datetime, date
        if not data_nascimento:
            return False
        
        try:
            # Se vier como string do formulário (ex: "1995-10-25"), converte para objeto date
            if isinstance(data_nascimento, str):
                dt = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
            else:
                dt = data_nascimento
            
            hoje = date.today()
            # Calcula a idade baseada no ano, ajustando caso não tenha feito aniversário ainda este ano
            idade = hoje.year - dt.year - ((hoje.month, hoje.day) < (dt.month, dt.day))
            return idade >= 18
        except Exception:
            return False
