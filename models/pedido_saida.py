from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class PedidoSaida(CrudBase):
    table = "pedido_saida"
    primary_key = "pedido_saida_id"
    fields= [
        "data_hora",
        "status_pedido",
        "descricao",  
        "cliente_id",
        "estoque_id",
        "funcionario_id"
    ]

    def __init__(self, status_pedido, descricao, cliente_id, funcionario_id, data_hora=None, estoque_id=None, id=None):
        self.id = id 
        self.data_hora = data_hora
        self.status_pedido = status_pedido
        self.descricao = descricao
        self.cliente_id = cliente_id
        self.funcionario_id = funcionario_id
        self.estoque_id = estoque_id

    def validate(self):
        erros = [
            Validator.required(self.cliente_id, "cliente_id"),
            Validator.required(self.data_hora, "data_hora"),
            Validator.required(self.status_pedido, "status_pedido"),
            Validator.required(self.estoque_id, "estoque_id"),
        ]
        return [erro for erro in erros if erro]