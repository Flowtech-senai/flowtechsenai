from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

# traz a tabela 'estoque' com os campos do banco
class Estoque(CrudBase):
    table = "estoque"
    primary_key = "estoque_id"
    fields = [
        "quantidade",
        "produto_id",
        "lote" 
    ]

    def __init__(self, quantidade=None, produto=None, lote=None, id=None):
        self.estoque_id = id 
        self.quantidade = quantidade
        self.produto_id = produto_id
        self.lote = lote

    def validate(self):
        erros = [
            Validator.required(self.quantidade, "quantidade"),
            Validator.required(self.produto_id, "produto_id"),
            Validator.required(self.lote, "lote"),
        ]
        return [erro for erro in erros if erro]


    # busca produto no estoque pelo id (lote do produto)
    @classmethod
    def has_related_records(cls, estoque_id):
        conexao = Database.connect()
        cursor = conexao.cursor(buffered=True)
        try:
            sql = f"SELECT COUNT(*) FROM {cls.table} WHERE {cls.primary_key} = %s"
            cursor.execute(sql, (estoque_id,))
            resultado = cursor.fetchone()
            total = resultado[0] if resultado else 0
            return total > 0 
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, estoque_id):
        if cls.has_related_records(estoque_id):
            return super().delete(estoque_id)
        raise ValueError("Estoque não encontrado ou já excluído.")


    
