from database import db, CRUD

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    
    def __init__(self, descricao):
        self.descricao = descricao
    
    def _repr_(self):
        return f"Perfil(id: {self.id}, descricao: {self.descricao})"
    
# Perfis como lista
def obter_todos_perfis():
    crud_perfil = CRUD(Perfil)
    perfis = crud_perfil.get_all()
    return perfis

# Id -> Descrição
def obter_perfil(id_perfil):
    perfis = obter_todos_perfis()
    for perfil in perfis:
        if perfil.id == id_perfil:
            return perfil.descricao   
    return None

# Descrição -> id
def obter_id_perfil(perfil_str):
    perfis = obter_todos_perfis()
    for perfil in perfis:
        if perfil.descricao == perfil_str:
            return perfil.id
    return None