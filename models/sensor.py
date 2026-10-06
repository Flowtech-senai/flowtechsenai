from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Sensor(CrudBase):
    table = "sensores"
    fields = [
        "id",
        "sensor_nome",
        "sensor_codigo",
        "sensor_tipo",
        "sensor_setor",
        "timestamp"
    ]

    def __init__(self, sensor_nome, sensor_codigo, sensor_tipo, sensor_setor, valor, timestamp=None, id=None):
        self._id = id 
        self.sensor_nome = sensor_nome
        self.sensor_codigo = sensor_codigo
        self.sensor_tipo = sensor_tipo
        self.sensor_setor = sensor_setor
        self.valor = valor
        self.timestamp = timestamp

    def validate(self):
        erros = [
            Validator.required(self.sensor_nome, "Nome do Sensor"),
            Validator.required(self.sensor_codigo, "Código do Sensor"),
            Validator.required(self.sensor_tipo, "Tipo do Sensor"),
            Validator.required(self.sensor_setor, "Setor do Sensor"),
            Validator.required(self.valor, "Valor da Leitura")
        ]
        return [erro for erro in erros if erro]

    @property
    def id(self):
        return self._id

    # Método para facilitar a transformação em dicionário para o JSON da API
    def to_dict(self):
        return {
            "id": self._id,
            "sensor_nome": self.sensor_nome,
            "sensor_codigo": self.sensor_codigo,
            "sensor_tipo": self.sensor_tipo,
            "sensor_setor": self.sensor_setor,
            "valor": self.valor,
            "timestamp": self.timestamp.isoformat() if hasattr(self.timestamp, 'isoformat') else str(self.timestamp) if self.timestamp else None
        }

    @classmethod
    def find_all(cls, order_by="timestamp DESC"):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table}"
            if order_by:
                sql += f" ORDER BY {order_by}"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            return [
                cls(
                    sensor_nome=row["sensor_nome"],
                    sensor_codigo=row["sensor_codigo"],
                    sensor_tipo=row["sensor_tipo"],
                    sensor_setor=row["sensor_setor"],
                    valor=row["valor"],
                    timestamp=row.get("timestamp"),
                    id=row["id"]
                ) for row in resultados
            ]
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def find_by_id(cls, sensor_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE id = %s"
            cursor.execute(sql, (sensor_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    sensor_nome=row["sensor_nome"],
                    sensor_codigo=row["sensor_codigo"],
                    sensor_tipo=row["sensor_tipo"],
                    sensor_setor=row["sensor_setor"],
                    valor=row["valor"],
                    timestamp=row.get("timestamp"),
                    id=row["id"]
                )
            return None
        finally:
            cursor.close()
            conexao.close()

    def delete(self):
        if not self._id:
            raise Exception("Não é possível deletar um sensor sem ID.")
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = f"DELETE FROM {self.table} WHERE id = %s"
            cursor.execute(sql, (self._id,))
            conexao.commit()
            return cursor.rowcount
        except Exception as e:
            conexao.rollback()
            raise Exception(f"Erro ao deletar o sensor do banco: {e}")
        finally:
            cursor.close()
            conexao.close()
