from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.estacao import Estacao
from models.setor import Setor
from database import CRUD
 
# Define the blueprint
estacao_bp = Blueprint('estacoes', __name__, template_folder="estacao")

# Página inicial das estacoes
@estacao_bp.route("/estacoes", methods=["GET"])
@login_required
def estacoes():
    crud_setores = CRUD(Setor)
    setores = crud_setores.get_all()
    # Criar uma lista para ser renderizada pelo html convertendo setor.id no seu setor.descricao correspondente
    setores_descricao = {setor.id: setor.descricao for setor in setores}   
    
    crud_estacao = CRUD(Estacao)
    estacoes = crud_estacao.get_all()
    
    return render_template("/adm/estacoes.html", estacoes = estacoes, setores_descricao = setores_descricao)

# Criar nova estacao
@estacao_bp.route("/estacao/criar", methods=["GET", "POST"])
@login_required
def criar():  
    crud_setores = CRUD(Setor)
    
    setores = crud_setores.get_all()
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        descricao = form_data.get("descricao")
        id_setor = form_data.get("id_setor")
        
        crud_estacao = CRUD(Estacao)
               
        estacao = crud_estacao.find("descricao", descricao)
        if estacao:
            flash("Estação já cadastrada!", "error")
            return render_template("estacao/criar.html", setores = setores)
        
        crud_estacao.create({"descricao": descricao, "id_setor" : id_setor})
    
        flash("Estação criado com suscesso!", "success")
        return redirect(url_for("estacoes.estacoes"))
    
    #request.method == "GET":
    return render_template("estacao/criar.html", setores = setores) 

# Editar perfil
@estacao_bp.route("/estacao/editar/<int:estacao_id>", methods=["GET", "POST"])
@login_required
def editar(estacao_id):
    crud_setores = CRUD(Setor)
    setores = crud_setores.get_all()
    
    crud_estacao = CRUD(Estacao)       
    estacao = crud_estacao.find("id", estacao_id)
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nova_descricao = form_data.get("descricao")
        novo_id_setor = form_data.get("id_setor")

        crud_estacao.update(estacao.id, {"descricao" : nova_descricao, "id_setor": novo_id_setor})
        
        flash("Estação editada com suscesso!", "success")
        return redirect(url_for("estacoes.estacoes"))
        
    # request.method == "GET":
    return render_template("estacao/editar.html", estacao = estacao, setores = setores)

# Excluir perfil
@estacao_bp.route("/estacao/excluir/<int:estacao_id>", methods=["GET", "POST"])
@login_required
def excluir(estacao_id):
    crud_estacao = CRUD(Estacao)
    
    estacao = crud_estacao.find("id", estacao_id)

    if request.method == "POST":
        crud_estacao.delete(estacao.id)
        
        flash(f"Estacão excluída com sucesso!", "success")
        return redirect(url_for("estacoes.estacoes"))

    # request.method == "GET":
    return render_template("estacao/excluir_confirmacao.html", estacao = estacao)