from database import db, CRUD

# Definição da classe
class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    
    # Inicialização da classe
    def __init__(self, descricao):
        self.descricao = descricao

    # Representação textual da classe
    def _repr_(self):
        return f"Setor(id: {self.id}, descricao: {self.descricao})"

# Cria um novo setor
def criar_setor(descricao):
    crud_setor = CRUD(Setor)
    crud_setor.create({"descricao": descricao})

# Atualiza o setor relacionado ao 'id'
def atualizar_setor(id, descricao):
    crud_setor = CRUD(Setor)
    crud_setor.update(id, {"descricao": descricao}) 
    
# Excluir o setor relacionado ao 'id'
def excluir_setor(id):
    crud_setor = CRUD(Setor)
    crud_setor.delete(id)

# Retona o setor relacionado a 'atributo' = 'valor' (ex. 'descricao' = 'Recepção')
def obter_setor(atributo, valor):
    crud_setor = CRUD(Setor)
    setor = crud_setor.find(atributo, valor)
    return setor

# Retorna todos os setores
def obter_todos_setores():
    crud_setor = CRUD(Setor)
    setores = crud_setor.get_all()
    return setores