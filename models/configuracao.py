from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Configuracao(CrudBase):

    # Nome da tabela no seu banco de dados MySQL/PostgreSQL
    table = "configuracao"
    primary_key = "configuracao_id"

    # Campos que pertencem à tabela configuracao no banco
    fields = [
        "funcionario_id",
        "tema",
        "notificacoes",
        "idioma"
    ]

    def __init__(
        self,
        funcionario_id,
        tema="claro",
        notificacoes=True,
        idioma="pt-BR",
        configuracao_id=None
    ):
        self.configuracao_id = configuracao_id
        self.funcionario_id = funcionario_id
        self.tema = tema
        self.notificacoes = notificacoes
        self.idioma = idioma

    def validate(self):
        
        """Realiza as validações dos campos antes de salvar.
        Retorna uma lista de mensagens de erro se houver problemas."""
        erros = []

        # 1. Validação de Funcionário obrigatório
        erro_funcionario = Validator.required(
            self.funcionario_id,
            "funcionario_id"
        )
        if erro_funcionario:
            erros.append(erro_funcionario)

        # 2. Validação do Tema
        if self.tema not in ["claro", "escuro"]:
            erros.append(
                "Tema inválido. Escolha entre 'claro' ou 'escuro'."
            )

        # 3. Validação do Idioma
        idiomas_validos = ["pt-BR", "en-US", "es-ES"]
        if self.idioma not in idiomas_validos:
            erros.append(
                "Idioma inválido."
            )

        # 4. Validação do campo Notificações
        if not isinstance(self.notificacoes, bool):
            erros.append(
                "O campo 'notificacoes' deve ser verdadeiro ou falso."
            )

        return erros

    @classmethod
    def buscar_por_funcionario(cls, funcionario_id):

        """Busca as configurações vinculadas a um funcionário específico.
        Retorna um dicionário com os dados salvos ou None.
        """
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"""
                SELECT *
                FROM {cls.table}
                WHERE funcionario_id = %s
                LIMIT 1
            """
            cursor.execute(sql, (funcionario_id,))
            return cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()