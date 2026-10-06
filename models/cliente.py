import re
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

# traz a tabela 'cliente' com os campos do banco
class Cliente(CrudBase):
    primary_key = "cliente_id"
    table = "cliente"
    fields = [
        "nome",
        "telefone",
        "cnpj",
        "e_mail",
        "endereco"
    ]

    def __init__(self, nome, telefone, cnpj, e_mail, endereco, id=None):
        self.id = id
        
        # Limpa espaços extras, remove números/símbolos e capitaliza o nome
        self.nome = self._limpar_e_capitalizar_nome(nome)
        
        # Garante que telefone e cnpj guardem APENAS os números puros no banco de dados
        self.telefone = self._apenas_numeros(telefone)
        self.cnpj = self._apenas_numeros(cnpj)
        
        # Padroniza o e-mail para minúsculo e remove espaços nas pontas
        self.e_mail = e_mail.strip().lower() if e_mail else ""
        
        # Remove espaços inúteis do endereço
        self.endereco = endereco.strip() if endereco else ""


    def validate(self):
        erros = []

        # 1. Validações básicas de campos obrigatórios (Usando suas funções nativas)
        erro_nome = Validator.required(self.nome, "nome")
        erro_cnpj = Validator.required(self.cnpj, "cnpj")
        erro_email = Validator.required(self.e_mail, "e_mail")

        if erro_nome: erros.append(erro_nome)
        if erro_cnpj: erros.append(erro_cnpj)
        if erro_email: erros.append(erro_email)

        # 2. Validações Locais de tamanho (Só rodam se o campo foi preenchido)
        if self.nome and len(self.nome) < 3:
            erros.append("O campo 'nome' deve conter um nome real com pelo menos 3 letras.")
            
        # TELEFONE: Validação local estrita de tamanho (11 dígitos)
        if self.telefone:
            if len(self.telefone) != 11:
                erros.append("O campo 'telefone' deve conter exatamente 11 números (DDD + celular).")
            else:
                # Se tiver 11 números, chama a API para ver se o formato/DDD existe de fato
                if not Validator.validar_telefone_externo_br(self.telefone):
                    erros.append("O número de 'telefone' informado não é válido ou o DDD não existe.")
        else:
            # Caso queira que o telefone também seja obrigatório, descomente a linha abaixo:
            # erros.append("O campo 'telefone' é obrigatório.")
            pass

        # 3. Validação do E-mail por API
        if self.e_mail and not erro_email:
            if not Validator.validar_email_externo_real(self.e_mail):
                erros.append("O e-mail informado não existe ou está desativado no servidor.")
                
        # 4. Validação do CNPJ por API
        if self.cnpj and not erro_cnpj:
            if len(self.cnpj) != 14:
                erros.append("O campo 'cnpj' deve conter exatamente 14 números.")
            else:
                # Só gasta crédito da API se passar no teste de 14 dígitos
                if not Validator.validar_cnpj_externo_receita(self.cnpj):
                    erros.append("O CNPJ fornecido não existe ou não está ativo na base da Receita Federal.")

        # 5. Retorna a lista com TODOS os erros encontrados juntos
        return [erro for erro in erros if erro]


    def _apenas_numeros(self, valor: str) -> str:
        if not valor:
            return ""
        return re.sub(r'\D', '', str(valor))

    def _limpar_e_capitalizar_nome(self, nome_bruto: str) -> str:
        if not nome_bruto:
            return ""
        # Remove números e caracteres especiais, mantendo letras acentuadas e espaços
        letras_e_espacos = re.sub(r'[^\w\s]', '', nome_bruto, flags=re.UNICODE)
        letras_e_espacos = re.sub(r'\d', '', letras_e_espacos)
        
        # Divide as palavras limpando espaços desnecessários
        palavras = letras_e_espacos.strip().split()
        conectores = {'de', 'da', 'do', 'das', 'dos', 'e'}
        
        return " ".join([p.lower() if p.lower() in conectores else p.capitalize() for p in palavras])

    # busca o cliente pelo id
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            # Corrigida a interpolação da String SQL que estava quebrada no seu código original
            sql = f"SELECT COUNT(*) FROM {cls.table} WHERE {cls.primary_key} = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0 
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        cliente = cls.find_by_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado.") 
        
        cls.delete(id)
