from database import db, CRUD

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    data_nascimento = db.Column(db.DateTime)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(255))
    sexo = db.Column(db.String(255))
    cpf = db.Column(db.String(14))
    
    def __init__(self, nome, data_nascimento, email, telefone, sexo, cpf):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone
        self.sexo = sexo
        self.cpf = cpf
    
    def _repr_(self):
        return f"Paciente(id: {self.id}, nome: {self.nome}, data_nascimento: {self.data_nascimento}, email: {self.data_nascimento}, telefone: {self.telefone}, sexo: {self.sexo}, cpf: {self.cpf})"
 
# Cria um novo paciente
def criar_paciente(nome, data_nascimento, email, telefone, sexo, cpf):
    crud_paciente = CRUD(Paciente)
    crud_paciente.create({"nome" : nome, "data_nascimento" : data_nascimento, "email" : email, "telefone" : telefone, "sexo" : sexo, "cpf": cpf})
   
# Retona o paciente relacionado a 'atributo' = 'valor' (ex. 'id' = 1, 'nome' = 'Rafael')
def obter_paciente(atributo, valor):
    crud_paciente = CRUD(Paciente)
    estacao = crud_paciente.find(atributo, valor)
    return estacao

# Atualiza o paciente  relacionado a 'id'
def atualizar_paciente(id, nome, data_nascimento, email, telefone, sexo, cpf):
    crud_paciente = CRUD(Paciente)
    crud_paciente.update(id, {"nome" : nome, "data_nascimento" : data_nascimento, "email" : email, "telefone" : telefone, "sexo" : sexo, "cpf": cpf})

# Excluir o paciente relacioando ao 'id'
def excluir_paciente(id):
    crud_paciente = CRUD(Paciente)
    crud_paciente.delete(id)

# Retorna todos os pacientes
def obter_todos_pacientes():
    crud_paciente = CRUD(Paciente)
    pacientes = crud_paciente.get_all()
    return pacientes
    
