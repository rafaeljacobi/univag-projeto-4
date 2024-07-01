import datetime
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from models.senha import criar_senha, obter_senha, obter_todas_senhas, obter_ultimas_senhas, excluir_senha, excluir_todas_senhas, obter_senhas_hoje
from models.setor import obter_setor, obter_todos_setores
from models.estacao import obter_estacao

# Blueprint para lidar com o totem de auto-atendimento e o painel de exibição da senhas
senha_bp = Blueprint("senhas", __name__, template_folder="senha")

# Parte 1 - administração das senhas
# Página administrativa das senhas
@senha_bp.route("/senhas", methods=["GET", "POST"]) 
@login_required
def senhas():
    setores = obter_todos_setores()
   
    # Criar um dicionário  para ser renderizada pelo html associando 'setor.id' a seu 'setor.descricao' correspondente
    setores_descricao = {setor.id: setor.descricao for setor in setores}   
    
    senhas = obter_todas_senhas()
    
    return render_template("adm/senhas.html", senhas = senhas, setores_descricao = setores_descricao)

# Excluir uma única senha baseada em 'senha_id'
@senha_bp.route("/senha/excluir/<int:senha_id>", methods=["GET", "POST"])
@login_required
def excluir(senha_id):
    senha = obter_senha("id", senha_id)
    print(f" Senha_id = {senha_id}")
    print("Senha = ")
    print(senha)
    # O POST é acionado quando o usuário confirma a exclusão em 'senha/excluir-senha-unica.html'
    if request.method == "POST":
        excluir_senha(senha.id)
        
        flash(f"Senha excluída com sucesso!", "success")
        return redirect(url_for("senhas.senhas"))
    
    # request.method == "GET" - renderiza a página de confirmação para exclusão
    return render_template("senha/excluir-senha-unica.html", senha = senha)

# Excluir todas as senhas do banco de dados
@senha_bp.route("/senha/excluir-tudo/", methods=["GET", "POST"])
@login_required
def excluir_tudo():
    # O POST é acionado quando o usuário confirma a exclusão em 'senha/excluir-todas-senhas.html'
    if request.method == "POST":
        excluir_todas_senhas()
        
        flash(f"Senhas excluídas com sucesso!", "success")
        return redirect(url_for("senhas.senhas"))
    
    # request.method == "GET":
    return render_template("senha/excluir-todas-senhas.html")


# Parte 2 - Geração da senhas no totem de auto-atendimento
# 1/3 - Escolher o setor disponível para atendimento
@senha_bp.route("/totem", methods=["GET", "POST"])
def totem():
    setores = obter_todos_setores()
     
    return render_template("/senha/totem.html", setores = setores)

# 2/3 - Escolher a categoria (convencional ou prioridade)
@senha_bp.route("/categoria/<int:setor_id>", methods=["GET", "POST"])
def categoria(setor_id):
    setor = obter_setor("id", setor_id)
    
    return render_template("senha/categoria.html", setor = setor)

# 3/3 - Obter a senha gerada - TODO: opção para imprimir a senha
@senha_bp.route("/senha/<int:setor_id>/<string:categoria>", methods=["GET", "POST"])
def senha(setor_id, categoria):
    # Data e hora da geração da senha
    data_hora_atual = datetime.datetime.now()
    data_atual = data_hora_atual.date()
    hora_atual = data_hora_atual.time()
    
    setor = obter_setor("id", setor_id)
    
    # Gera uma nova senha de acordo com a categoria e setor
    senha = gerar_senha(categoria, setor.id)
    
    # Cria a nova senha
    criar_senha(setor_id, senha, categoria, data_hora_atual)
       
    # Gera a página com o resultado da nova senha (formatada em número de 4 dígitos = 0000) e data e hora no formato habitual
    return render_template("senha/senha_gerada.html", 
                           numero = str(senha).zfill(4), 
                           categoria = categoria, 
                           setor = setor.descricao, 
                           data = data_atual.strftime("%Y-%m-%d"), 
                           hora = hora_atual.strftime("%H:%M:%S"))

# Gera uma nova senha seguindo o fluxo:
# 1. Seleciona as senhas já existentes de acordo com o setor
# 2. Seleciona as senhas do setor de acordo com a categoria
# 3. Ordena em ordem crescente as senhas por seu número
# 4. Acresceta 1 ao maior valor obtido
def gerar_senha(categoria, senha_id):
    nova_senha = 0
    
    # Versão 1
    #senhas = obter_todas_senhas()
    
    # Versão 2
    senhas = obter_senhas_hoje()

    senhas_filtradas = list(filter(lambda senha: senha.id_setor == senha_id and senha.categoria == categoria, senhas))
    if senhas_filtradas:
        senhas_ordenadas = sorted(senhas_filtradas, key = lambda s: s.numero)
        ultima_senha = senhas_ordenadas.pop()
        nova_senha = ultima_senha.numero + 1
    else:
        nova_senha = 1
    
    return nova_senha

# Seleciona as 4 últimas senhas chamadas para a recepção, sendo que a mais recente vai ficar em destaque.
@senha_bp.route("/senha/ultimas_senhas/", methods=["GET", "POST"])
def ultimas_senhas_recepcao():
    setor = obter_setor("descricao", "Recepção")
    
    senhas_selecionadas = obter_ultimas_senhas(setor.id)
    
    senhas_formatadas = []
    for senha in senhas_selecionadas:
        if senha.categoria == "Convencional":
            numero = "C-" + str(senha.numero).zfill(4)
        else: # senha.categoria == "Prioridade":
            numero = "P-" + str(senha.numero).zfill(4)
        
        # Formata a senha como um dicionário com as senhas para ser renderizado pela página html e javascript
        senha_data = {
            "setor": "Recepção",
            "numero": numero,
            "estacao":  obter_estacao("id", senha.id_estacao).descricao
        }
        senhas_formatadas.append(senha_data) 
  
    return render_template("senha/painel-senhas-geral.html", senhas = senhas_formatadas)

# Atualiza a interface das senhas no painel de senhas geral
@senha_bp.route("/senha/recepcao/auto-refresh", methods=["GET", "POST"])
def auto_refresh():
    setor = obter_setor("descricao", "Recepção")
    
    senhas_selecionadas = obter_ultimas_senhas(setor.id)
   
    senhas_formatadas = []
    for senha in senhas_selecionadas:
        if senha.categoria == "Convencional":
            numero = "C-" + str(senha.numero).zfill(4)
        else: # senha.categoria == "Prioridade":
            numero = "P-" + str(senha.numero).zfill(4)
        
        # Formata a senha como um dicionário com as senhas para ser renderizado pela página html e javascript
        senha_data = {
            "setor": "Recepção",
            "numero": numero,
            "estacao": obter_estacao("id", senha.id_estacao).descricao
        }
        senhas_formatadas.append(senha_data)

    # Retorna senhas_formatadas no formato JSON
    return senhas_formatadas
