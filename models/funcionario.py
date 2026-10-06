import re
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


class Funcionario(CrudBase):
    table = "funcionario"
    primary_key = "funcionario_id"

    fields = [
        "nome",
        "CPF",
        "e_mail",
        "setor",
        "cargo",
        "salario",
        "turno",
        "senha",
        "telefone",
        "data_nascimento"
    ]

    def __init__(
        self,
        nome,
        CPF,
        e_mail,
        setor,
        cargo,
        salario,
        turno,
        senha,
        telefone,
        data_nascimento,
        funcionario_id=None
    ):
        self.funcionario_id = funcionario_id
        self.nome = nome
        self.CPF = CPF
        self.e_mail = e_mail
        self.setor = setor
        self.cargo = cargo
        self.salario = salario
        self.turno = turno
        self.senha = senha
        self.telefone = telefone
        self.data_nascimento = data_nascimento

    def validate(self):
        erros = []

        # FORMATAÇÃO AUTOMÁTICA

        if self.nome:
            self.nome = self.nome.strip().title()

        if self.telefone:
            self.telefone = re.sub(r'\D', '', str(self.telefone))

        if self.CPF:
            self.CPF = re.sub(r'\D', '', str(self.CPF))

        # CAMPOS OBRIGATÓRIOS

        erro_nome = Validator.required(self.nome, "nome")
        erro_cpf = Validator.required(self.CPF, "CPF")
        erro_email = Validator.required(self.e_mail, "e_mail")
        erro_data = Validator.required(
            self.data_nascimento,
            "data_nascimento"
        )
        erro_salario = Validator.required(self.salario, "salario")

        if erro_nome:
            erros.append(erro_nome)

        if erro_cpf:
            erros.append(erro_cpf)

        if erro_email:
            erros.append(erro_email)

        if erro_data:
            erros.append(erro_data)

        if erro_salario:
            erros.append(erro_salario)

        # VALIDAÇÃO DO NOME

        if self.nome and not erro_nome:
            if len(self.nome.replace(" ", "")) < 3:
                erros.append(
                    "O campo 'nome' deve conter um nome real "
                    "com pelo menos 3 letras."
                )

        # VALIDAÇÃO DO TELEFONE

        if self.telefone:
            if len(self.telefone) != 11:
                erros.append(
                    "O campo 'telefone' deve conter exatamente "
                    "11 números (DDD + celular)."
                )
            else:
                if not Validator.validar_telefone_externo_br(
                    self.telefone
                ):
                    erros.append(
                        "O número de 'telefone' informado não é "
                        "válido ou o DDD não existe."
                    )

        # VALIDAÇÃO DO E-MAIL

        if self.e_mail and not erro_email:
            if not Validator.validar_email_externo_real(
                self.e_mail
            ):
                erros.append(
                    "O e-mail informado é inválido. "
                    "Ele deve conter um '@' e pelo menos um "
                    "ponto '.' após o arroba."
                )

        # VALIDAÇÃO DO CPF

        if self.CPF and not erro_cpf:
            if len(self.CPF) != 11:
                erros.append(
                    "O campo 'CPF' deve conter exatamente "
                    "11 números."
                )
            else:
                if not Validator.validar_cpf_real(self.CPF):
                    erros.append(
                        "O CPF fornecido não é válido."
                    )

        
        # VALIDAÇÃO DA IDADE

        if self.data_nascimento and not erro_data:
            if not Validator.validar_maioridade(
                self.data_nascimento
            ):
                erros.append(
                    "O funcionário deve ser maior de 17 anos "
                    "(mínimo de 18 anos completos)."
                )

        # VALIDAÇÃO DO SALÁRIO

        if self.salario and not erro_salario:
            erro_val_salario = Validator.non_negative(
                self.salario,
                "salario"
            )

            if erro_val_salario:
                erros.append(erro_val_salario)

        return erros

    # AUTENTICAÇÃO

    @classmethod
    def autenticar(cls, email, senha):
        conexao = Database.connect()

        cursor = conexao.cursor(
            dictionary=True,
            buffered=True
        )

        try:
            sql = f"""
                SELECT *
                FROM {cls.table}
                WHERE e_mail = %s
                AND senha = %s
                LIMIT 1
            """

            cursor.execute(sql, (email, senha))

            funcionario = cursor.fetchone()

            return funcionario

        finally:
            cursor.close()
            conexao.close()

    # VERIFICAR SE FUNCIONÁRIO EXISTE

    @classmethod
    def exists(cls, funcionario_id):
        """Retorna True se o funcionário existir no banco."""

        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = f"""
                SELECT COUNT(*)
                FROM {cls.table}
                WHERE funcionario_id = %s
            """

            cursor.execute(sql, (funcionario_id,))

            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

    # EXCLUIR FUNCIONÁRIO COM SEGURANÇA

    @classmethod
    def safe_delete(cls, funcionario_id):
        if not cls.exists(funcionario_id):
            raise ValueError(
                "funcionario não encontrado."
            )

        return super().delete(funcionario_id)
