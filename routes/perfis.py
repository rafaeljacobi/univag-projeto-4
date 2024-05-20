from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.perfil import Perfil
from database import CRUD
 
# Blueprint para lidar com o perfil
perfil_bp = Blueprint("perfis", __name__, template_folder="perfil")
 
# Página inicial do perfil
@perfil_bp.route("/perfis", methods=["GET"])
@login_required
def perfis():
    crud_perfil = CRUD(Perfil)
    
    perfis = crud_perfil.get_all()
    
    return render_template("adm/perfis.html", perfis = perfis)

# Criar novo perfil
@perfil_bp.route("/perfil/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        descricao = form_data.get("descricao")
        
        crud_perfil = CRUD(Perfil)
               
        perfil = crud_perfil.find("descricao", descricao)
        if perfil:
            flash("Perfil já cadastrado!", "error")
            return render_template("perfil/criar.html")
        
        crud_perfil.create({"descricao": descricao})
    
        flash("Perfil criado com suscesso!", "success")
        return redirect(url_for("perfis.perfis"))
    
    #request.method == "GET":
    return render_template("perfil/criar.html") 

# Editar perfil
@perfil_bp.route("/perfil/editar/<int:perfil_id>", methods=["GET", "POST"])
@login_required
def editar(perfil_id):
    crud_perfil = CRUD(Perfil)
        
    perfil = crud_perfil.find("id", perfil_id)
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nova_descricao = form_data.get("descricao")       

        crud_perfil.update(perfil.id, {"descricao" : nova_descricao})
        
        flash("Perfil editador com suscesso!", "success")
        return redirect(url_for("perfis.perfis"))
        
    # request.method == "GET":
    return render_template("perfil/editar.html", perfil = perfil)

# Excluir perfil
@perfil_bp.route("/perfil/excluir/<int:perfil_id>", methods=["GET", "POST"])
@login_required
def excluir(perfil_id):
    crud_perfil = CRUD(Perfil)
    
    perfil = crud_perfil.find("id", perfil_id)
    
    if request.method == "POST":
        crud_perfil.delete(perfil.id)
        
        flash(f"Perfil excluído com sucesso!", "success")
        return redirect(url_for("perfis.perfis"))
    
    # request.method == "GET":
    return render_template("perfil/excluir-confirmacao.html", perfil = perfil)