from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from models.usuario import obter_usuario, criar_usuario, atualizar_usuario
from models.perfil import obter_todos_perfis
from util import conferir_senha, criar_senha
 
# Blueprint para lidar com as autenticações
auth_bp = Blueprint("auth", __name__, template_folder="auth")

# Login do sistema
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        email = form_data.get("email")
        senha = form_data.get("senha")
        
        usuario = obter_usuario("email", email)
        if usuario and conferir_senha(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for("usuarios.base"))
        else:
            flash("E-mail e\ou senha inválidos.", "error")

    # request.method == "GET":
    return render_template("auth/login.html")

# Cria um novo usuário
# Acesso restrito ao perfil de Administrador
# TODO: criar um usuario temporáril para ser 'devolvido' a auth\registrar.html para que o usuário não 
#       precise reiniciar tudo novamente nas situações de erro.
@auth_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    perfis = obter_todos_perfis()   
    
    usuario = current_user
       
    if not usuario.is_adm():
        flash("Apenas usuários com o perfil 'Administrador' podem acessar essa funcionalidade!", "error")
        return redirect(url_for("usuarios.index"))
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nome = form_data.get("nome")
        email = form_data.get("email")
        senha = form_data.get("senha")
        confirma_senha = form_data.get("confirmar_senha")
        id_perfil = int(form_data.get("id_perfil"))   # O retorno da página é o perfil.id correspondente
               
        usuario = obter_usuario("email", email)
        if usuario:
            flash("Endereço de E-mail já em uso! Escolha um diferente ou contate o administrador do sistema.", "error")
            return render_template("auth/registrar.html", perfis = perfis)
        
        if senha != confirma_senha:
            flash("As senhas informadas são diferentes entre sí! Tente novamente!.", "error")
            return render_template("auth/registrar.html", perfis = perfis)
       
        criar_usuario({"nome": nome, "email": email, "senha": criar_senha(senha), "id_perfil": id_perfil})
        
        flash("Usuario criado com suscesso!", "success")
        return redirect(url_for("usuarios.usuarios"))

    # request.method == "GET":
    return render_template("auth/registrar.html", perfis = perfis)

# Mudar senha do usuário atual
@auth_bp.route("/mudar_senha", methods=["GET", "POST"])
@login_required
def mudar_senha():
    if request.method == "POST":
        form_data = request.form.to_dict()

        senha_atual = form_data.get("senha_atual")
        nova_senha = form_data.get("nova_senha")
        confirmar_senha = form_data.get("confirmar_senha")
              
        usuario = obter_usuario("id", current_user.id)
        
        if not conferir_senha(usuario.senha, senha_atual):
            flash("Senha atual incorreta!", "error")
            return redirect(url_for("auth.mudar_senha"))

        if nova_senha != confirmar_senha:
            flash("As novas senhas não coincidem!", "warning")
            return redirect(url_for("auth.mudar_senha"))

        # Atualiza apenas a senha
        atualizar_usuario(usuario.id, usuario.nome, usuario.email, criar_senha(nova_senha), usuario.id_perfil)

        flash("Senha atualizada com suscesso!", "success")   
        return redirect(url_for("usuarios.profile"))
    
    # request.method == "GET":
    return render_template("auth/mudar_senha.html")

# Logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("usuarios.index"))