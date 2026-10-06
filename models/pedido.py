from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Pedido(CrudBase):
    table = "movimentacao"
    primary_key = "movimentacao_id"
    fields = [
        "data_horamov",
        "tipo_mov",
        "quantidade",
        "observacao",
        "estoque_id",
        "funcionario_id"
    ]

    def __init__(self, data_horamov, tipo_mov, quantidade, observacao, estoque_id, funcionario_id, id=None):
        self.id = id 
        self.data_horamov = data_horamov
        self.tipo_mov = tipo_mov
        self.quantidade = quantidade
        self.observacao = observacao
        self.estoque_id = estoque_id
        self.funcionario_id = funcionario_id

    def validate(self):
        erros = [
            Validator.required(self.data_horamov, "data_horamov"),
            Validator.required(self.tipo_mov, "tipo_mov"),
            validator.required(self.quantidade, "quantidade"),
            Validator.required(self.estoque_id, "estoque_id"),
            Validator.required(self.funcionario_id, "funcionario_id"),
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def has_related_records(cls, pedido_id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
        
            sql = "SELECT COUNT(*) FROM movimentacao WHERE movimentacao_id = %s"
            cursor.execute(sql, (movimentacao_id,))
            total = cursor.fetchone()[0]
            return total == 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, movimentacaoo_id):
        movimentacao = cls.find_by_id(movimentacao_id)
        if not movimentacao:
            raise ValueError("pedido não encontrado.")
        
        return super().delete(movimentacao_id)
