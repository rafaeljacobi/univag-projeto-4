from database import db, CRUD

class Senha(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_setor = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer)
    categoria = db.Column(db.Enum("Convencional", "Prioridade"))
    data_hora = db.Column(db.DateTime)
        
    def __init__(self, id_setor, numero, categoria, data_hora):
        self.id_setor = id_setor
        self.numero = numero
        self.categoria = categoria
        self.data_hora = data_hora
        
    def __json__(self):
        return {
            "numero": str(self.numero).zfill(4),
            "categoria": self.categoria,
            "data_hora": self.data_hora.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _repr_(self):
        return f"Senha(id: {self.id}, id_setor: {self.id_setor}, numero: {self.numero}, categoria: {self.categoria}, data: {self.data}, hora: {self.hora})"
    
# Todas as senhas como lista
def obter_todas_senhas():
    crud_senha = CRUD(Senha)
    senhas = crud_senha.get_all()
    return senhas

# Todas as senhas de acordo com a categoria como lista
def obter_todas_senhas_por_categoria(categoria):
    crud_senha = CRUD(Senha)
    senhas = crud_senha.find("categoria", categoria)
    return senhas