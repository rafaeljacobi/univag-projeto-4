from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.setor import obter_todos_setores, obter_setor, criar_setor, atualizar_setor, excluir_setor
 
 # Blueprint para lidar com setor
setor_bp = Blueprint("setores", __name__, template_folder="setor")

# Página administrativa dos setores
@setor_bp.route("/setores", methods=["GET"])
@login_required
def setores():  
    setores = obter_todos_setores()

    return render_template("adm/setores.html", setores=setores)

# Cria um novo setor
@setor_bp.route("/setores/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        descricao = form_data.get("descricao")
               
        setor  = obter_setor("descricao", descricao)
        if setor:
            flash("Setor já cadastrado!", "error")
            return render_template("setor/criar.html")
        
        criar_setor({"descricao": descricao})
    
        flash("Setor criado com suscesso!", "success")
        return redirect(url_for("setores.setores"))
    
    #request.method == "GET":
    return render_template("setor/criar.html") 

# Edita setor relacionado ao 'setor_id'
@setor_bp.route("/setor/editar/<int:setor_id>", methods=["GET", "POST"])
@login_required
def editar(setor_id):
        
    setor = obter_setor("id", setor_id)
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nova_descricao = form_data.get("descricao")       

        atualizar_setor(setor.id, {"descricao" : nova_descricao})
        
        flash("Setor  editador com suscesso!", "success")
        return redirect(url_for("setores.setores"))
        
    # request.method == "GET":
    return render_template("setor/editar.html", setor = setor)

@setor_bp.route("/setor/excluir/<int:setor_id>", methods=["GET", "POST"])
@login_required
def excluir(setor_id):  
    setor =obter_setor("id", setor_id)
    
    if request.method == "POST":
        excluir_setor(setor.id)
        
        flash(f"Setor excluído com sucesso!", "success")
        return redirect(url_for("setores.setores"))
    
    # request.method == "GET":
    return render_template("setor/excluir-confirmacao.html", setor = setor)