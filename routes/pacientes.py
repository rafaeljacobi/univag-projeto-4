import datetime
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.paciente import obter_todos_pacientes, obter_paciente, criar_paciente, atualizar_paciente, excluir_paciente
from models.senha import obter_senha, atualizar_senha_chamada
  
# Blueprint para lidar com o perfil
paciente_bp = Blueprint("pacientes", __name__, template_folder="paciente")
 
# Página administrativa dos pacientes
@paciente_bp.route("/pacientes", methods=["GET"])
@login_required
def pacientes():  
    pacientes = obter_todos_pacientes()
    
    return render_template("adm/pacientes.html", pacientes = pacientes)

# Cria um novo paciente via admnistrador
@paciente_bp.route("/paciente/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":       
        form_data = request.form.to_dict()
        
        cpf = form_data.get("cpf")
        nome = form_data.get("nome")
        data_nascimento_str = form_data.get("data_nascimento")
        data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%Y-%m-%d")
        email = form_data.get("email")
        telefone = form_data.get("telefone")
        sexo = form_data.get("sexo")
                      
        paciente = obter_paciente("nome", nome)
        if paciente:
            flash("Paciente já cadastrado!", "error")
            return render_template("paciente/criar.html")
        
        criar_paciente(nome, data_nascimento, email, telefone, sexo, cpf)
    
        flash("Paciente criado com suscesso!", "success")
        return redirect(url_for("pacientes.pacientes"))
    
    #request.method == "GET":
    return render_template("paciente/criar.html") 

# Cria um novo paciente via recepcao
@paciente_bp.route("/paciente/recepcao_criar/<int:setor_id>/<int:estacao_id>/<int:senha_atual_id>/<string:cpf>", methods=["GET", "POST"])
@login_required
def recepcao_criar(setor_id, estacao_id, senha_atual_id, cpf):
    senha = obter_senha("id", senha_atual_id)
    
    if request.method == "POST":
        atualizar_senha_chamada(senha.id, None, "Atendendo")
        
        form_data = request.form.to_dict()
        
        cpf = form_data.get("cpf")
        nome = form_data.get("nome")
        data_nascimento_str = form_data.get("data_nascimento")
        data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%Y-%m-%d")
        email = form_data.get("email")
        telefone = form_data.get("telefone")
        sexo = form_data.get("sexo")
                      
        paciente = obter_paciente("nome", nome)
        if paciente:
            flash("Paciente já cadastrado!", "error")
            return render_template("paciente/criar.html", setor_id, estacao_id, senha_atual_id, cpf)
        
        criar_paciente(nome, data_nascimento, email, telefone, sexo, cpf)
    
        flash("Paciente criado com suscesso!", "success")
        return redirect(url_for("recepcao.senhas", setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id, acao = "encerrar_atendimento"))
    
    #request.method == "GET":
    return render_template("paciente/criar.html", setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id, cpf = cpf) 

# Edita o paciente relacionado ao 'paciente_id'
@paciente_bp.route("/paciente/editar/<int:paciente_id>", methods=["GET", "POST"])
@login_required
def editar(paciente_id):
    paciente = obter_paciente("id", paciente_id)
    data_nascimento = paciente.data_nascimento.strftime("%Y-%m-%d")

    if request.method == "POST":
        form_data = request.form.to_dict()
        
        cpf = form_data.get("cpf")
        nome = form_data.get("nome")
        data_nascimento_str = form_data.get("data_nascimento")
        data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%Y-%m-%d")
        email = form_data.get("email")
        telefone = form_data.get("telefone")
        sexo = form_data.get("sexo")

        atualizar_paciente(paciente.id, nome, data_nascimento, email, telefone, sexo, cpf)
        
        flash("Paciente atualizado com suscesso!", "success")
        return redirect(url_for("pacientes.pacientes"))
        
    # request.method == "GET":
    return render_template("paciente/editar.html", paciente = paciente, data_nascimento = data_nascimento)



# Edita o paciente relacionado ao 'paciente_id' via recepção
@paciente_bp.route("/paciente/recepcao_editar/<int:paciente_id>/<int:setor_id>/<int:estacao_id>/<int:senha_atual_id>", methods=["GET", "POST"])
@login_required
def recepcao_editar(paciente_id, setor_id, estacao_id, senha_atual_id):
    paciente = obter_paciente("id", paciente_id)
    data_nascimento = paciente.data_nascimento.strftime("%Y-%m-%d")
        
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        cpf = form_data.get("cpf")
        nome = form_data.get("nome")
        data_nascimento_str = form_data.get("data_nascimento")
        data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%Y-%m-%d")
        email = form_data.get("email")
        telefone = form_data.get("telefone")
        sexo = form_data.get("sexo")

        atualizar_paciente(paciente.id, nome, data_nascimento, email, telefone, sexo, cpf)
        
        flash("Paciente atualizado com suscesso!", "success")
        return redirect(url_for("recepcao.senhas", setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id, acao = 'encerrar_atendimento'))
        
    # request.method == "GET":
    return render_template("paciente/editar.html", paciente = paciente, data_nascimento = data_nascimento, setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id)

# Exclui o paciente relacionado a 'paciente_id'
@paciente_bp.route("/paciente/excluir/<int:paciente_id>", methods=["GET", "POST"])
@login_required
def excluir(paciente_id): 
    paciente = obter_paciente("id", paciente_id)
    
    if request.method == "POST":
        excluir_paciente(paciente.id)
        
        flash(f"Paciente excluído com sucesso!", "success")
        return redirect(url_for("pacientes.pacientes"))
    
    # request.method == "GET":
    return render_template("paciente/excluir-confirmacao.html", paciente = paciente)

# Pesquisa o paciente relacionado a 'cpf'
@paciente_bp.route("/paciente/pesquisar/<int:setor_id>/<int:estacao_id>/<int:senha_atual_id>", methods=["GET", "POST"])
@login_required
def pesquisar(setor_id, estacao_id, senha_atual_id): 
   
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        cpf = form_data.get("cpf")
        #setor_id = form_data.get("setor_id")
        #estacao_id = form_data.get("estacao_id")
        #senha_atual_id = form_data.get("senha_atual_id")
        
        paciente = obter_paciente("cpf", cpf)
        if paciente:
            return redirect(url_for("pacientes.recepcao_editar", paciente_id = paciente.id, setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id, cpf = paciente.cpf))
        else:
            return redirect(url_for("pacientes.recepcao_criar", setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id, cpf = cpf))
            
    # request.method == "GET":
    return render_template("paciente/pesquisar.html", setor_id = setor_id, estacao_id = estacao_id, senha_atual_id = senha_atual_id)
