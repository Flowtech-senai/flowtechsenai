import re
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

# traz a tabela 'cliente' com os campos do banco
class Perfil(CrudBase):
    primary_key = "funcionario_id"
    table = "funcionario"
    fields = [
        "nome",
        "data_nascimento"
    ]

    def __init__(self, nome, data_nascimento, id=None):
        self.id = id
        self.nome = self._limpar_e_capitalizar_nome(nome)
        self.telefone = self._apenas_numeros(telefone)


    def validate(self):
        erros = []

        erro_nome = Validator.required(self.nome, "nome")

        if erro_nome: erros.append(erro_nome)

        if self.nome and len(self.nome) < 3:
            erros.append("O campo 'nome' deve conter um nome real com pelo menos 3 letras.")


    def _apenas_numeros(self, valor: str) -> str:
        if not valor:
            return ""
        return re.sub(r'\D', '', str(valor))

    def _limpar_e_capitalizar_nome(self, nome_bruto: str) -> str:
        if not nome_bruto:
            return ""
        # Remove números e caracteres especiais, mantendo letras acentuadas e espaços
        letras_e_espacos = re.sub(r'[^\w\s]', '', nome_bruto, flags=re.UNICODE)
        letras_e_espacos = re.sub(r'\d', '', letras_e_espacos)
        
        # Divide as palavras limpando espaços desnecessários
        palavras = letras_e_espacos.strip().split()
        conectores = {'de', 'da', 'do', 'das', 'dos', 'e'}
        
        return " ".join([p.lower() if p.lower() in conectores else p.capitalize() for p in palavras])

    # busca o usuario pelo id
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            # Corrigida a interpolação da String SQL que estava quebrada no seu código original
            sql = f"SELECT COUNT(*) FROM {cls.table} WHERE {cls.primary_key} = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0 
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        cliente = cls.find_by_id(id)
        if not cliente:
            raise ValueError("Usuário não encontrado.") 
        
        cls.delete(id)

        # Validação da Idade 
        if self.data_nascimento and not erro_data:
            if not Validator.validar_maioridade(self.data_nascimento):
                erros.append("O funcionário deve ser maior de 17 anos (mínimo de 18 anos completos).")
