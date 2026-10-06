from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class PedidoEntrada(CrudBase):
    table = "pedido_entrada"
    primary_key = "pedido_entrada_id"
    fields = [
        "data_hora",
        "descricao", 
        "status_pedido", 
        "fornecedor_id",
        "local_id",
        "funcionario_id",
        "rfid"
    ]

    def __init__(self, descricao, status_pedido, fornecedor_id, funcionario_id, data_hora=None, data_entrada=None, local_id=None, estoque_id=None, rfid=None, id=None):
        self.id = id 
        self.data_hora = data_hora if data_hora is not None else data_entrada
        self.descricao = descricao
        self.status_pedido = status_pedido
        self.fornecedor_id = fornecedor_id
        self.funcionario_id = funcionario_id
        self.local_id = local_id if local_id is not None else estoque_id
        self.rfid = rfid

    def validate(self):
        erros = [
            Validator.required(self.fornecedor_id, "fornecedor_id"),
            Validator.required(self.data_hora, "data_hora"),
            Validator.required(self.status_pedido, "status_pedido"),
            Validator.required(self.local_id, "local_id"),
            Validator.required(self.rfid, "rfid"), 
        ]
        return [erro for erro in erros if erro]
