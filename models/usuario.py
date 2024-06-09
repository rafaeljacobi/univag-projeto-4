from flask_login import UserMixin
from database import db, CRUD

# Definição da classe
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_perfil = db.Column(db.Integer, nullable=False)
    id_estacao = db.Column(db.Integer)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    
    # Inicialização da classe
    def __init__(self, nome, email, senha, id_perfil):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.id_perfil = id_perfil

    # Representação textual da classe
    def _repr_(self):
        return f"Users(id: {self.id}, nome: {self.nome}, email: {self.email}, password: {self.password}, id_perfil: {self.id_perfil})"

    # Usuário é administrador ?
    def is_adm(self):
        if self.perfil_str() == "Administrador":
            return True
        return False
    
    # Retorna o objeto perfil relacionado ao 'id_perfil' do usuário
    def perfil_str(self):
        from models.perfil import obter_perfil_id
        perfil = obter_perfil_id(self.id_perfil)
        return perfil

# Cria um novo usuário 
def criar_usuario(nome, email, senha, id_perfil):
    crud_usuario = CRUD(Usuario)
    crud_usuario.create({"nome": nome, "email": email, "senha": senha, "id_perfil": id_perfil})
    
# Atualiza o usuário relacionada ao 'id'
def atualizar_usuario(id, nome, email, senha, id_perfil):
    crud_usuario = CRUD(Usuario)
    crud_usuario.update(id, {"nome": nome, "email": email, "senha": senha, "id_perfil": id_perfil})
    
# Exclui o usuário relacionado ao 'id'
def excluir_usuario(id):
    crud_usuario = CRUD(Usuario)
    crud_usuario.delete(id)

# Retona o usuário relacionado a 'atributo' = 'valor' (ex. 'id' = 1, 'nome' = 'Rafael')
def obter_usuario(atributo, valor):
    crud_usuario = CRUD(Usuario)
    usuario = crud_usuario.find(atributo, valor)
    return usuario

# Retorna todos os usuarios
def obter_todos_usuarios():
    crud_usuarios = CRUD(Usuario)
    usuarios = crud_usuarios.get_all()
    return usuarios