from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Produto(CrudBase):
    table = "produto"
    fields = [
        "produto_id",
        "nome",
        "categoria",
        "tipo_produto",
        "estoque_minimo",
        "validade",
        "lote",
        "localizacao",
        "RFID",
        "descricao",
        "fornecedor",
        "foto" # <-- ADICIONADO na lista de campos do banco
    ]

    # ADICIONADO: foto=None no final dos parâmetros do __init__
    def __init__(self, nome, categoria, tipo_produto, estoque_minimo,
                    validade, lote, localizacao, RFID, descricao, fornecedor, foto=None, produto_id=None):
        self.produto_id = produto_id
        self.nome = nome
        self.categoria = categoria
        self.tipo_produto = tipo_produto
        self.estoque_minimo = estoque_minimo
        self.validade  = validade
        self.lote = lote
        self.localizacao = localizacao
        self.RFID = RFID
        self.descricao = descricao
        self.fornecedor = fornecedor
        self.foto = foto # <-- ADICIONADO mapeamento do atributo interno

    def validate(self):
        erros = [
            Validator.required(self.nome, "Nome"),
            Validator.required(self.categoria, "Categoria"),
            Validator.required(self.tipo_produto, "Tipo de Produto"),
            Validator.non_negative(self.estoque_minimo, "Estoque Mínimo"),
            Validator.required(self.validade, "Validade"),
            Validator.required(self.lote, "Lote"),
            Validator.required(self.localizacao, "Localização"),
            Validator.required(self.RFID, "RFID"),
            Validator.required(self.descricao, "Descrição"),
            Validator.required(self.fornecedor, "Fornecedor")
            # A foto não foi colocada como required aqui porque ela pode ser opcional ou ignorada na edição
        ]
        return [erro for erro in erros if erro]

    @property
    def id(self):
        return self.produto_id

    @classmethod
    def find_all(cls, order_by=None):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto"
            if order_by:
                sql += f" ORDER BY {order_by}"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            return [
                cls(
                    nome=row["nome"],
                    categoria=row["categoria"],
                    tipo_produto=row["tipo_produto"],
                    estoque_minimo=row["estoque_minimo"],
                    validade=row["validade"],
                    lote=row["lote"],
                    localizacao=row["localizacao"],
                    RFID=row["RFID"],
                    descricao=row["descricao"],
                    fornecedor=row.get("fornecedor", "N/I"),
                    foto=row.get("foto"), # <-- ADICIONADO ao puxar a lista de produtos
                    produto_id=row["produto_id"]
                ) for row in resultados
            ]
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def exclusao_segura(cls, produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE `produto` SET `ativo` = 0 WHERE `produto_id` = %s" 
            cursor.execute(sql, (produto_id,))
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            raise Exception(f"Erro ao atualizar o banco: {e}")
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def has_related_records(cls, produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_movimentacao WHERE produto_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (produto_id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()
            
    @classmethod
    def find_by_id(cls, produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto WHERE produto_id = %s"
            cursor.execute(sql, (produto_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    nome=row["nome"],
                    categoria=row["categoria"],
                    tipo_produto=row["tipo_produto"],
                    estoque_minimo=row["estoque_minimo"],
                    validade=row["validade"],
                    lote=row["lote"],
                    localizacao=row["localizacao"],
                    RFID=row["RFID"],
                    descricao=row["descricao"],
                    fornecedor=row.get("fornecedor", "N/I"),
                    foto=row.get("foto"), # <-- ADICIONADO ao buscar produto único por ID
                    produto_id=row["produto_id"]
                )
            return None
        finally:
            cursor.close()
            conexao.close()

    def delete(self):
        if not self.produto_id:
            raise Exception("Não é possível deletar um produto sem ID.")
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM produto WHERE produto_id = %s"
            cursor.execute(sql, (self.produto_id,))
            conexao.commit()
            return cursor.rowcount
        except Exception as e:
            conexao.rollback()
            raise Exception(f"Erro ao deletar o produto do banco: {e}")
        finally:
            cursor.close()
            conexao.close()
