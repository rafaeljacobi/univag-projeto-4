import datetime
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.senha import Senha
from models.setor import Setor, obter_todos_setores
from database import CRUD

# Blueprint para lidar com o totem de auto-atendimento
senha_bp = Blueprint("senhas", __name__, template_folder="senha")

# Página inicial das senhas - administrativo
@senha_bp.route("/senhas", methods=["GET", "POST"])
@login_required
def senhas():
    # request.method == "GET"
    crud_setores = CRUD(Setor)
    setores = crud_setores.get_all()
    
    # Criar uma lista para ser renderizada pelo html convertendo setor.id no seu setor.descricao correspondente
    setores_descricao = {setor.id: setor.descricao for setor in setores}   
    
    crud_senhas = CRUD(Senha)
    senhas = crud_senhas.get_all()
    
    return render_template("/adm/senhas.html", senhas = senhas, setores_descricao = setores_descricao)

# Excluir uma única senha
@senha_bp.route("/senha/excluir/<int:senha_id>", methods=["GET", "POST"])
@login_required
def excluir(senha_id):
    crud_senha = CRUD(Senha)
    
    senha = crud_senha.find("id", senha_id)
        
    if request.method == "POST":
        crud_senha.delete(senha.id)
        
        flash(f"Senha excluída com sucesso!", "success")
        return redirect(url_for("senhas.senhas"))
    
    # request.method == "GET":
    return render_template("senha/excluir-senha-unica.html", senha = senha)

# Excluir todas as senhas
@senha_bp.route("/senha/excluir-tudo/", methods=["GET", "POST"])
@login_required
def excluir_tudo():
    crud_senha = CRUD(Senha) 
        
    if request.method == "POST":
        crud_senha.delete_all()
        
        flash(f"Senhas excluídas com sucesso!", "success")
        return redirect(url_for("senhas.senhas"))
    
    # request.method == "GET":
    return render_template("senha/excluir-todas-senhas.html")


# O fluxo para o paciente gerar a senha é o seguinte:
# 1/3 - Escolher o setor disponível para atendimento
@senha_bp.route("/totem", methods=["GET", "POST"])
def totem():
    # request.method == "GET" 
    setores = obter_todos_setores()
    
    return render_template("/senha/totem.html", setores = setores)

# 2/3 - Escolher a categoria (convencional ou prioridade)
@senha_bp.route("/categoria/<int:senha_id>", methods=["GET", "POST"])
def categoria(senha_id):
    # request.method == "GET"
    crud_setor = CRUD(Setor)
    setor = crud_setor.find("id", senha_id)
    
    return render_template("senha/categoria.html", setor = setor)

# 3/3 - Obter a senha gerada - TODO: opção para imprimir a senha
@senha_bp.route("/senha/<int:senha_id>/<string:categoria>", methods=["GET", "POST"])
def senha(senha_id, categoria):

    # Registra a data e hora da geração da senha
    data_hora_atual = datetime.datetime.now()
    data_atual = data_hora_atual.date()
    hora_atual = data_hora_atual.time()
    
    # Obtem o respectivo setor selecionado pelo usuário
    crud_setor = CRUD(Setor)
    setor = crud_setor.find("id", senha_id)
    
    # Gera uma nova senha de acordo com a categoria e setor
    senha = gerar_senha(categoria, setor.id)
    
    # Registra a nova senha
    crud_senha = CRUD(Senha)
    crud_senha.create({"id_setor": senha_id, "numero": senha, "categoria": categoria, "data_hora": data_hora_atual})
       
    # Gera a página com o resultado da nova senha (formatada em número de 4 dígitos = 0000) e data e hora no formato habitual
    return render_template("senha/senha_gerada.html", 
                           numero = str(senha).zfill(4), 
                           categoria = categoria, 
                           setor = setor.descricao, 
                           data = data_atual.strftime("%Y-%m-%d"), 
                           hora = hora_atual.strftime("%H:%M:%S"))

# Gera uma nova senha seguindo o fluxo:
# - Seleciona as senhas já existentes de acordo com o setor
# - Seleciona as senhas do setor de acordo com a categoria
# - Ordena em ordem crescente as senhas por seu número
# - Acresceta 1 ao maior valor
def gerar_senha(categoria, senha_id):
    nova_senha = 0
    
    crud_senha = CRUD(Senha)
    senhas = crud_senha.get_all()
    senhas_filtradas = list(filter(lambda senha: senha.id_setor == senha_id and senha.categoria == categoria, senhas))
    if senhas_filtradas:
        senhas_ordenadas = sorted(senhas_filtradas, key = lambda s: s.numero)
        ultima_senha = senhas_ordenadas.pop()
        nova_senha = ultima_senha.numero + 1
    else:
        nova_senha = 1
    
    return nova_senha
