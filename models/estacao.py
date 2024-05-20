from database import db, CRUD

class Estacao(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_setor = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer)
    descricao = db.Column(db.String(255), nullable=False)
 
    def __init__(self, descricao, id_setor):
        self.descricao = descricao
        self.id_setor = id_setor
    
    def _repr_(self):
        return f"Estacao(id: {self.id}, descricao: {self.descricao}, id_setor: {self.id_setor}, id_usuario: {self.id_usuario})"
    
# Estacoes como lista
def obter_todas_estacoes():
    crud_estacao = CRUD(Estacao)
    estacoes = crud_estacao.get_all()
    return estacoes