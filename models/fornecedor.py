import re
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Fornecedor(CrudBase):
    table = "fornecedor"
    primary_key = "fornecedor_id"
    fields = [
        "nome",
        "cnpj",
        "telefone",
        "e_mail",
        "endereco"
    ]

    def __init__(self, nome, cnpj, telefone, e_mail, endereco, id=None):
        self.id = id 
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.e_mail = e_mail
        self.endereco = endereco
   
    def validate(self):
        erros = []

        # --- FORMATÇÃO AUTOMÁTICA ---
        if self.nome:
            self.nome = self.nome.strip().title()  # Ex: "empresa ltda" -> "Empresa Ltda"

        if self.telefone:
            import re
            self.telefone = re.sub(r'\D', '', str(self.telefone)) # Deixa apenas números

        # --- VALIDAÇÕES DE CAMPOS OBRIGATÓRIOS ---
        erro_nome = Validator.required(self.nome, "nome")
        erro_cnpj = Validator.required(self.cnpj, "cnpj")
        erro_email = Validator.required(self.e_mail, "e_mail")

        if erro_nome: erros.append(erro_nome)
        if erro_cnpj: erros.append(erro_cnpj)
        if erro_email: erros.append(erro_email)

        # --- VALIDAÇÕES LOCAIS ---
        # Nome com no mínimo 3 letras
        if self.nome and not erro_nome:
            if len(self.nome.replace(" ", "")) < 3:
                erros.append("O campo 'nome' deve conter um nome real com pelo menos 3 letras.")
            
        # Telefone estrito com 11 números
        if self.telefone:
            if len(self.telefone) != 11:
                erros.append("O campo 'telefone' deve conter exatamente 11 números (DDD + celular).")
            else:
                if not Validator.validar_telefone_externo_br(self.telefone):
                    erros.append("O número de 'telefone' informado não é válido ou o DDD não existe.")

        # --- VALIDAÇÕES EXTERNAS (APIs) ---
        if self.e_mail and not erro_email:
            if not Validator.validar_email_externo_real(self.e_mail):
                erros.append("O e-mail informado não existe ou está desativado no servidor.")
                
        if self.cnpj and not erro_cnpj:
            if len(self.cnpj) != 14:
                erros.append("O campo 'cnpj' deve conter exatamente 14 números.")
            else:
                if not Validator.validar_cnpj_externo_receita(self.cnpj):
                    erros.append("O CNPJ fornecido não existe ou não está ativo na base da Receita Federal.")

        return erros



    @classmethod
    def exists(cls, fornecedor_id):
        """Retorna True se o fornecedor existir no banco."""
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "SELECT COUNT(*) FROM fornecedor WHERE fornecedor_id = %s"
            cursor.execute(sql, (fornecedor_id,))
            total = cursor.fetchone()[0]
            return total > 0  # Corrigido: retorna True se achar o registro
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, fornecedor_id):
        if not cls.exists(fornecedor_id):
            raise ValueError("Fornecedor não encontrado.")
        return super().delete(fornecedor_id)
