from database import db, CRUD

# Definição da classe 
class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    
    # Inicialização da classe
    def __init__(self, descricao):
        self.descricao = descricao
    
    # Representação textual da classe
    def _repr_(self):
        return f"Perfil(id: {self.id}, descricao: {self.descricao})"

# Cria um novo perfil
def criar_perfil(descricao):
    crud_perfil = CRUD(Perfil)
    crud_perfil.create({"descricao": descricao})
    
# Atualiza o perfil relacionado ao 'id'
def atualizar_perfil(id, descricao):
    crud_perfil = CRUD(Perfil)
    crud_perfil.update(id, {"descricao": descricao})

# Retorna todos os perfis
def obter_todos_perfis():
    crud_perfil = CRUD(Perfil)
    perfis = crud_perfil.get_all()
    return perfis

# Retona o perfil relacionado a 'atributo' = 'valor' (ex. 'id' = 1, 'descricao' = 'Recepção')
def obter_perfil(atributo, valor):
    crud_perfil = CRUD(Perfil)
    perfil = crud_perfil.find(atributo, valor)
    return perfil

# Excluir o perfil relacionado ao 'id'
def excluir_perfil(id):
    crud_perfil = CRUD(Perfil)
    crud_perfil.delete(id)

# Função auxiliar para gerar os primeiros usuários testes: ID->Descricao
def obter_perfil_id(id_perfil):
    perfis = obter_todos_perfis()
    for perfil in perfis:
        if perfil.id == id_perfil:
            return perfil.descricao   
    return None

# Função auxiliar para gerar os primeiros usuários testes: Descricao->Id
def obter_id_perfil(perfil_str):
    perfis = obter_todos_perfis()
    for perfil in perfis:
        if perfil.descricao == perfil_str:
            return perfil.id
    return None