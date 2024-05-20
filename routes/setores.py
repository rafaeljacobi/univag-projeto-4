from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.setor import Setor
from database import CRUD
 
 # Blueprint para lidar com setor
setor_bp = Blueprint("setores", __name__, url_prefix="/setor")

# Página inicial do perfil
@setor_bp.route("/setores", methods=["GET"])
@login_required
def setores():
    crud_setor = CRUD(Setor)
    
    setores = crud_setor.get_all()

    return render_template("adm/setores.html", setores=setores)

@setor_bp.route("/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        descricao = form_data.get("descricao")
        
        crud_setor = CRUD(Setor)
               
        setor  = crud_setor.find("descricao", descricao)
        if setor:
            flash("Setor já cadastrado!", "error")
            return render_template("setor/criar.html")
        
        crud_setor.create({"descricao": descricao})
    
        flash("Setor criado com suscesso!", "success")
        return redirect(url_for("setores.setores"))
    
    #request.method == "GET":
    return render_template("setor/criar.html") 

# Editar setor
@setor_bp.route("/editar/<int:setor_id>", methods=["GET", "POST"])
@login_required
def editar(setor_id):
    crud_setor = CRUD(Setor)
        
    setor = crud_setor.find("id", setor_id)
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nova_descricao = form_data.get("descricao")       

        crud_setor.update(setor.id, {"descricao" : nova_descricao})
        
        flash("Setor  editador com suscesso!", "success")
        return redirect(url_for("setores.setores"))
        
    # request.method == "GET":
    return render_template("setor/editar.html", setor = setor)

@setor_bp.route("/excluir/<int:setor_id>", methods=["GET", "POST"])
@login_required
def excluir(setor_id):
    crud_setor = CRUD(Setor)
    
    setor = crud_setor.find("id", setor_id)
    print(f"Setor_id = {setor_id}")
    print(setor)
    
    if request.method == "POST":
        crud_setor.delete(setor.id)
        
        flash(f"Setor excluído com sucesso!", "success")
        return redirect(url_for("setores.setores"))
    
    # request.method == "GET":
    return render_template("setor/excluir-confirmacao.html", setor = setor)