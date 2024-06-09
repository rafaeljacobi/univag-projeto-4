from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.estacao import obter_estacao, obter_todas_estacoes, criar_estacao, atualizar_estacao, excluir_estacao
from models.setor import obter_todos_setores
from models.usuario import obter_todos_usuarios
 
# Blueprint para lidar com as estações
estacao_bp = Blueprint('estacoes', __name__, template_folder="estacao")

# Página administrativa das estações
@estacao_bp.route("/estacoes", methods=["GET"])
@login_required
def estacoes():
    # Criar um dicionário para ser renderizada pelo html associando setor.id no seu setor.descricao correspondente
    setores = obter_todos_setores()
    setores_descricao = {setor.id: setor.descricao for setor in setores}   
     
    # Criar um dicionário para ser renderizada pelo html associando usuario.id ao usuario.nome correspondente
    usuarios = obter_todos_usuarios()
    usuarios_descricao = {}
    for usuario in usuarios:
        if usuario.id_estacao is None:
            usuario_nome = "Estação Livre"
        else:
            usuario_nome = usuario.nome
        usuarios_descricao[usuario.id] = usuario_nome
    
    estacoes = obter_todas_estacoes()
    
    return render_template("/adm/estacoes.html", estacoes = estacoes, setores = setores_descricao, usuarios = usuarios_descricao)

# Criar nova estacao
@estacao_bp.route("/estacao/criar", methods=["GET", "POST"])
@login_required
def criar():  
    setores = obter_todos_setores()
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        descricao = form_data.get("descricao")
        id_setor = form_data.get("id_setor")
       
        estacao = obter_estacao("descricao", descricao)
        if estacao:
            flash("Estação já cadastrada!", "error")
            return render_template("estacao/criar.html", setores = setores)
        
        criar_estacao(descricao, id_setor)
    
        flash("Estação criado com suscesso!", "success")
        return redirect(url_for("estacoes.estacoes"))
    
    # request.method == "GET":
    return render_template("estacao/criar.html", setores = setores) 

# Editar perfil
@estacao_bp.route("/estacao/editar/<int:estacao_id>", methods=["GET", "POST"])
@login_required
def editar(estacao_id):   
    setores = obter_todos_setores()
    
    estacao = obter_estacao("id", estacao_id)
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nova_descricao = form_data.get("descricao")
        novo_id_setor = form_data.get("id_setor")

        atualizar_estacao(estacao.id, nova_descricao, novo_id_setor)
        
        flash("Estação editada com suscesso!", "success")
        return redirect(url_for("estacoes.estacoes"))
        
    # request.method == "GET":
    return render_template("estacao/editar.html", estacao = estacao, setores = setores)

# Excluir perfil
@estacao_bp.route("/estacao/excluir/<int:estacao_id>", methods=["GET", "POST"])
@login_required
def excluir(estacao_id):  
    estacao = obter_estacao("id", estacao_id)

    if request.method == "POST":
        excluir_estacao(estacao.id)
        
        flash(f"Estacão excluída com sucesso!", "success")
        return redirect(url_for("estacoes.estacoes"))

    # request.method == "GET":
    return render_template("estacao/excluir_confirmacao.html", estacao = estacao)