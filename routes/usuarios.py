from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from models.usuario import obter_todos_usuarios, obter_usuario, atualizar_usuario, excluir_usuario
from models.perfil import obter_perfil, obter_perfil_id, obter_todos_perfis
 
# Blueprint para lidar com os usuários
# Evitei pré-definir a rota com o url_prefix por conta da página inicial do sistema que é roteada neste blueprint
# TODO: Considerar criar uma nova página inicial para facilitar a entrada para testes
usuario_bp = Blueprint("usuarios", __name__, template_folder="usuarios")

# Página inicial do sistema (index principal)
@usuario_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Página principal de administração dos módulos do sistema
@usuario_bp.route("/adm", methods=["GET", "POST"])
@login_required
def adm():
    usuario = current_user
    
    if not usuario.is_adm():
        flash("Apenas usuários com o perfil 'Administrador' podem acessar essa funcionalidade!", "error")
        return redirect(url_for("usuarios.index"))
    
    return render_template("adm/index.html")

# Retorna a página principal de acordo com o perfil do usuário
@usuario_bp.route("/base", methods=["GET", "POST"])
@login_required
def base():
    usuario = current_user
    
    perfil = obter_perfil("id", usuario.id_perfil)
    
    if perfil.descricao == "Administrador":
        return redirect(url_for("usuarios.adm"))
    elif perfil.descricao == "Recepcionista":
        return redirect(url_for("recepcao.index"))
    else:
        return redirect(url_for("usuarios.index"))

# Gerencia os usuários do banco de dados - apenas o perfil Administrador pode acessar
@usuario_bp.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():
    usuario = current_user
    
    if not usuario.is_adm():
        flash("Apenas usuários com o perfil 'Administrador' podem acessar essa funcionalidade!", "warning")
        return redirect(url_for("usuarios.index"))

    usuarios = obter_todos_usuarios()
    return render_template("adm/usuarios.html", usuarios = usuarios)

# Profile (perfil pessoal) do usuário
@usuario_bp.route("/usuario/profile", methods=["GET", "POST"])
@login_required
def profile():
    usuario = current_user
    perfil_str = obter_perfil_id(usuario.id_perfil)    # Representação do código do perfil, ex. 1 = Administrador
    return render_template("usuario/profile.html", usuario = usuario, perfil_str = perfil_str)
 
# Editar profile - nome, email e perfil do usuário (adm, recepcionista, ...). 
# A senha apenas o próprio usuário pode mudar em outro módulo (página profile).
@usuario_bp.route("/usuario/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar(usuario_id):
    perfis = obter_todos_perfis()
    
    usuario = obter_usuario("id", usuario_id)
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        nome = form_data.get("nome")
        email = form_data.get("email")
        id_perfil = int(form_data.get("id_perfil"))       

        atualizar_usuario(usuario.id, {"nome": nome, "email": email, "id_perfil": id_perfil})
        
        flash("Usuário atualizado com suscesso!", "success")
        if usuario.is_adm():
            return redirect(url_for("usuarios.usuarios"))
        else:
            return redirect(url_for("usuarios.profile"))
        
    # request.method == "GET":
    return render_template("usuario/editar.html", usuario = usuario, perfis = perfis)

# Exclui o usuário "usuario_id", exceto se ele for o único usuário do banco de dados ou o próprio usuário atual
# No caso de ser o usuário atual tentando se excluir, a interface html já tem uma restrição para tal (o botão excluir 
# não aparece para o próprio usuário )
@usuario_bp.route("/usuario/excluir/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def excluir(usuario_id):   
    usuario = obter_usuario("id", usuario_id)
    
    if request.method == "POST":
        excluir_usuario(usuario_id)
    
        flash("Usuário excluído com sucesso!", "success")
        return redirect(url_for("usuarios.usuarios"))
    
    # request.method == "GET":
    return render_template("usuario/excluir-confirmacao.html", usuario = usuario)
