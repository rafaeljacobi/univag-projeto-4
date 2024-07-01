import datetime
from database import db, CRUD

# Definição da classe
class Senha(db.Model):   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_setor = db.Column(db.Integer, nullable=False)
    id_estacao = db.Column(db.Integer)
    numero = db.Column(db.Integer)
    categoria = db.Column(db.Enum("Convencional", "Prioridade"))
    status = db.Column(db.Enum("Aguardando", "Chamando", "Atendendo", "Encerrado")) 
    data_hora = db.Column(db.DateTime)
    
    # Inicialização da classe
    def __init__(self, id_setor, numero, categoria, data_hora, status):
        self.id_setor = id_setor
        self.numero = numero
        self.categoria = categoria
        self.data_hora = data_hora
        self.status = status
    
    # Converte a instância da classe em um dicionário no formato JSON
    def __json__(self):
        return {
            "id": self.id,
            "numero": str(self.numero).zfill(4),
            "categoria": self.categoria,
            "data_hora": self.data_hora.strftime("%Y-%m-%d %H:%M:%S")
        }

    # Representação textual da classe
    def _repr_(self):
        return f"Senha(id: {self.id}, id_setor: {self.id_setor}, numero: {self.numero}, categoria: {self.categoria}, data: {self.data}, hora: {self.hora})"

# Cria uma nova senha
def criar_senha(setor_id, numero, categoria, data_hora_atual):
    crud_senha = CRUD(Senha)
    crud_senha.create({"id_setor": setor_id, "numero": numero, "categoria": categoria, "data_hora": data_hora_atual, "status": "Aguardando"})

# Atualiza a senha relacionada ao 'id'
def atualizar_senha(id, id_setor, id_estacao, numero, categoria, data_hora, status):
    crud_senha = CRUD(Senha)
    crud_senha.update(id, {"id_setor": id_setor, id_estacao: id_estacao, "numero": numero, "categoria": categoria, "data_hora": data_hora, "status": status})

# Versão para atualizar apenas as chamadas de senha pela recepção
def atualizar_senha_chamada(id, id_estacao, status):
    crud_senha = CRUD(Senha)
    crud_senha.update(id, {"id_estacao": id_estacao, "status": status})
    
# Versão para atualizar apenas a hora da senha (chamar novamente)
def atualizar_hora_senha_chamada(id, data_hora):
    crud_senha = CRUD(Senha)
    crud_senha.update(id, {"data_hora": data_hora})
    
# Retona a senha relacionada a 'atributo' = 'valor' (ex. 'id' = 1)
def obter_senha(atributo, valor):
    crud_senha = CRUD(Senha)
    senha = crud_senha.find(atributo, valor)
    return senha

# Retorna todas as senhas
def obter_todas_senhas():
    crud_senha = CRUD(Senha)
    senhas = crud_senha.get_all()
    return senhas

# Retorna todas as senhas do dia de hoje
def obter_senhas_hoje(): 
    # 2024-07-01 07:59:53.970447
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
    print(data_atual)
    senhas = obter_todas_senhas()
    print(senhas)
    #senhas_hoje = Senha.query.filter(Senha.data_hora >= data_atual).all()
    #senhas_hoje = list(filter(lambda senha: senha.data_hora >= data_atual, senhas))
    senhas_hoje = []
    for senha in senhas:
        data_senha = senha.data_hora.strftime("%Y-%m-%d")
        print(data_senha)
        if data_senha >= data_atual:
            senhas_hoje.append(senha)
    print(senhas_hoje) 
    return senhas_hoje

# Excluir a senha relacionada ao 'id'
def excluir_senha(id):
    crud_senha = CRUD(Senha)
    crud_senha.delete(id)

# Exclui todas as senhas
def excluir_todas_senhas():
    crud_senha = CRUD(Senha)
    crud_senha.delete_all()

# Retonar as últimas senhas chamadas ordenadas em ordem decrescente
def obter_ultimas_senhas(id_setor, total = 4):
    # Versão 1
    #senhas = obter_todas_senhas()
    
    # Versão 2
    senhas = obter_senhas_hoje()
    
    senhas_selecionadas = []
    for senha in senhas:
        if senha.id_setor == id_setor:
            if senha.status in ("Chamando", "Atendendo", "Encerrado"):
                senhas_selecionadas.append(senha)
                
    # Ordenar por 'senha.data_hora' (decrescente)
    senhas_selecionadas.sort(key=lambda senha: senha.data_hora, reverse=True)
   
    # Limita o retorno ao total especificado de senhas
    senhas_selecionadas = senhas_selecionadas[:total]

    return senhas_selecionadas
