from database import db

class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(db.Integer, nullable=False)
    id_estacao = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum("Aguardando", "Atendendo", "Encerrado", "Cancelado"))
    data = db.Column(db.DateTime)
    hora = db.Column(db.DateTime)
   
    def __init__(self, id_paciente, id_estacao, status, data, hora):
        self.id_paciente = id_paciente
        self.id_estacao = id_estacao
        self.status = status
        self.data = data
        self.hora = hora
    
    def _repr_(self):
        return f"Atendimento(id: {self.id}, id_paciente: {self.id_paciente}, id_estacao: {self.id_estacao}, status: {self.status}, data: {self.data}, hora: {self.hora})"