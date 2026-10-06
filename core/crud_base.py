from core.database import Database

class CrudBase:
    table = ""
    fields = []
    primary_key = "id"  # Nome padrão da PK

    @classmethod
    def find_all(cls, order_by=None):
        # Se não passar ordem, usa a chave primária da classe
        order_field = order_by if order_by else cls.primary_key
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} ORDER BY {order_field}"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def find_by_id(cls, id_value): # busca por id o que estiver sendo solicitado 
        conexao = Database.connect() # conexão com banco de dados
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE {cls.primary_key} = %s" # seleciona tudo de alguma tabela de acordo com o id
            cursor.execute(sql, (id_value,))
            return cursor.fetchone() # fetchone é buscar por apenas um item
        finally:
            cursor.close() 
            conexao.close() # para a conexão

    @classmethod
    def delete(cls, id_value): # deleta de acordo com o id
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = f"DELETE FROM {cls.table} WHERE {cls.primary_key} = %s" # deleta da tabela o id solicitado
            cursor.execute(sql, (id_value,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()


    def insert(self): # insere na tabela
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            colunas = ", ".join(self.fields)
            marcadores = ", ".join(["%s"] * len(self.fields))
            # Pega os valores dos atributos listados em self.fields
            valores = tuple(getattr(self, campo) for campo in self.fields)
            sql = f"INSERT INTO {self.table} ({colunas}) VALUES ({marcadores})" # insere na tabela x na coluna y os valores que forem atribuídos
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    def update(self, id_value):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            campos = ", ".join([f"{campo} = %s" for campo in self.fields])
            valores = tuple(getattr(self, campo) for campo in self.fields) + (id_value,)
            sql = f"UPDATE {self.table} SET {campos} WHERE {self.primary_key} = %s"
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()
            


    @classmethod
    def find_by_field(cls, field_name, value):
        conexao = None
        cursor = None
        try:
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True, buffered=True)
            
            # Usamos UPPER e TRIM para ignorar maiúsculas/minúsculas e espaços invisíveis
            sql = f"SELECT * FROM {cls.table} WHERE UPPER(TRIM({field_name})) = UPPER(TRIM(%s))"
            cursor.execute(sql, (value,))
            
            return cursor.fetchone()
            
        except Exception as e:
            print(f"Erro ao buscar no banco: {e}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()




