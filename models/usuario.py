from flask_login import UserMixin
from database import db, CRUD

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_perfil = db.Column(db.Integer, nullable=False)
    id_estacao = db.Column(db.Integer)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    
    def __init__(self, nome, email, senha, id_perfil):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.id_perfil = id_perfil

    def _repr_(self):
        return f"Users(id: {self.id}, nome: {self.nome}, email: {self.email}, password: {self.password}, id_perfil: {self.id_perfil})"

    def is_adm(self):
        if self.perfil_str() == "Administrador":
            return True
        return False
    
    def perfil_str(self):
        from models.perfil import obter_perfil
        perfil = obter_perfil(self.id_perfil)
        return perfil

# Retornar uma lista com todos os registros
def obter_todos_usuarios():
    crud_usuarios = CRUD(Usuario)
    usuarios = crud_usuarios.get_all()
    return usuarios