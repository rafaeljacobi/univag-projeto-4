from flask import Blueprint, render_template, url_for, request, redirect, flash, jsonify
from flask_login import login_required
from models.estacao import Estacao
from models.setor import Setor, obter_todos_setores
from models.senha import Senha, obter_todas_senhas
from database import CRUD

# Blueprint para lidar com o módulo da recepção
recepcao_bp = Blueprint('recepcao', __name__, url_prefix="/recepcao")

# Página inicial do painel de senhas - lista os setores disponíveis
@recepcao_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    # request.method == "GET"
    setores = obter_todos_setores()
    
    return render_template("/recepcao/selecionar_setor.html", setores = setores)

# Página iniciar para lidar com as senhas
@recepcao_bp.route("/<int:setor_id>", methods=["GET", "POST"])
@login_required
def senhas(setor_id):
    # request.method == "GET"
    crud_setor = CRUD(Setor)
    setor = crud_setor.find("id", setor_id)
    
    crud_senhas = CRUD(Senha)
    senhas = crud_senhas.get_all()
    senhas_json = [senha.__json__() for senha in senhas]
    
    return render_template("recepcao/senhas.html", setor = setor, senhas = senhas_json)

# Rota para atualizar a interface das senhas
@recepcao_bp.route('/auto-refresh')
def auto_refresh():

    crud_senhas = CRUD(Senha)
    senhas = crud_senhas.get_all()
    senhas_json = [senha.__json__() for senha in senhas]
    
    return jsonify(senhas_json)