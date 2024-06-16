from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.perfil import obter_todos_perfis, obter_perfil, criar_perfil, atualizar_perfil, excluir_perfil
  
# Blueprint para lidar com o perfil
perfil_bp = Blueprint("perfis", __name__, template_folder="perfil")
 
# Página administrativa do perfil
@perfil_bp.route("/perfis", methods=["GET"])
@login_required
def perfis():  
    perfis = obter_todos_perfis()
    
    return render_template("adm/perfis.html", perfis = perfis)

# Cria um novo perfil
@perfil_bp.route("/perfil/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        descricao = form_data.get("descricao")
                      
        perfil = obter_perfil("descricao", descricao)
        if perfil:
            flash("Perfil já cadastrado!", "error")
            return render_template("perfil/criar.html")
        
        criar_perfil(descricao)
    
        flash("Perfil criado com suscesso!", "success")
        return redirect(url_for("perfis.perfis"))
    
    #request.method == "GET":
    return render_template("perfil/criar.html") 

# Edita perfil relacionado ao 'perfil_id'
@perfil_bp.route("/perfil/editar/<int:perfil_id>", methods=["GET", "POST"])
@login_required
def editar(perfil_id):        
    perfil = obter_perfil("id", perfil_id)
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nova_descricao = form_data.get("descricao")       

        atualizar_perfil(perfil.id, nova_descricao)
        
        flash("Perfil editador com suscesso!", "success")
        return redirect(url_for("perfis.perfis"))
        
    # request.method == "GET":
    return render_template("perfil/editar.html", perfil = perfil)

# Exclui o perfil relacionado a 'perfil_id'
@perfil_bp.route("/perfil/excluir/<int:perfil_id>", methods=["GET", "POST"])
@login_required
def excluir(perfil_id):   
    perfil = obter_perfil("id", perfil_id)
    
    if request.method == "POST":
        excluir_perfil(perfil.id)
        
        flash(f"Perfil excluído com sucesso!", "success")
        return redirect(url_for("perfis.perfis"))
    
    # request.method == "GET":
    return render_template("perfil/excluir-confirmacao.html", perfil = perfil)