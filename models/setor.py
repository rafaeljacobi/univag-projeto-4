from database import db, CRUD

class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    
    def __init__(self, descricao):
        self.descricao = descricao

    def _repr_(self):
        return f"Setor(id: {self.id}, descricao: {self.descricao})"
    
# Usuarios como lista
def obter_todos_setores():
    crud_setor = CRUD(Setor)
    setores = crud_setor.get_all()
    return setores