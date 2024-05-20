from database import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    data_nascimento = db.Column(db.DateTime)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(255))
    
    def __init__(self, nome, data_nascimento, email, telefone):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone
    
    def _repr_(self):
        return f"Paciente(id: {self.id}, nome: {self.nome}, data_nascimento: {self.data_nascimento}, email: {self.data_nascimento}, telefone: {self.telefone})"