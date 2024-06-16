from database import db, CRUD

# Definição da classe
class Estacao(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_setor = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer)
    descricao = db.Column(db.String(255), nullable=False)
 
    # Inicialização da classe
    def __init__(self, descricao, id_setor):
        self.descricao = descricao
        self.id_setor = id_setor
    
    # Representação textual da instância da classe
    def _repr_(self):
        return f"Estacao(id: {self.id}, descricao: {self.descricao}, id_setor: {self.id_setor}, id_usuario: {self.id_usuario})"

# Cria uma nova estação
def criar_estacao(descricao, id_setor):
    crud_estacao = CRUD(Estacao)
    crud_estacao.create({"descricao": descricao, "id_setor": id_setor})

# Retona a estação relacionada a 'atributo' = 'valor' (ex. 'id' = 1, 'descricao' = 'Recepção')
def obter_estacao(atributo, valor):
    crud_estacao = CRUD(Estacao)
    estacao = crud_estacao.find(atributo, valor)
    return estacao

# Atualiza a estação relacionada a 'id'
def atualizar_estacao(id, descricao, setor_id):
    crud_estacao = CRUD(Estacao)
    crud_estacao.update(id, {"descricao" : descricao, "id_setor": setor_id})

# Atualiza a estação relacionada a 'id'
def selecionar_estacao(id, id_usuario):
    crud_estacao = CRUD(Estacao)
    crud_estacao.update(id, {"id_usuario" : id_usuario})

# Excluir a estação relacioanda ao 'id'
def excluir_estacao(id):
    crud_estacao = CRUD(Estacao)
    crud_estacao.delete(id)

# Retorna todas as estações
def obter_todas_estacoes():
    crud_estacao = CRUD(Estacao)
    estacoes = crud_estacao.get_all()
    return estacoes