import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.estacao import obter_todas_estacoes, obter_estacao, selecionar_estacao
from models.setor import obter_todos_setores, obter_setor
from models.senha import obter_todas_senhas, atualizar_senha_chamada, obter_senha, atualizar_hora_senha_chamada, obter_senhas_hoje
from models.usuario import obter_todos_usuarios

# Blueprint para lidar com o módulo da recepção
recepcao_bp = Blueprint('recepcao', __name__, url_prefix="/recepcao")

# Página para selecionar os setores disponíveis para a recepção
@recepcao_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    # request.method == "GET"
    usuario = current_user
    
    # Avalia se o usuario já stá vinculado a alguma estação e desfaz a associação
    estacao = obter_estacao("id_usuario", usuario.id)
    if estacao:
        selecionar_estacao(estacao.id, None)
    
    setores = obter_todos_setores()
    
    # Etapa 1 - usuário seleciona o setor
    return render_template("/recepcao/selecionar-setor.html", setores = setores)

# Página para selecionar as estações disponíveis para a recepção
@recepcao_bp.route("/<int:setor_id>", methods=["GET", "POST"])
@login_required
def estacoes(setor_id):
    # request.method == "GET"
    setor = obter_setor("id", setor_id)
   
    estacoes = obter_todas_estacoes()
    
    # Seleciona as estações que correspondem ao 'setor_id'
    estacoes_selecionadas = filter(lambda estacao: estacao.id_setor == setor.id, estacoes)

    usuarios = obter_todos_usuarios()
    usuarios_descricao = {usuario.id: usuario.nome for usuario in usuarios}  
    
    # Etapa 2 - usuário seleciona a estação de trabalho
    return render_template("recepcao/selecionar-estacao.html", setor = setor, estacoes = estacoes_selecionadas, usuarios = usuarios_descricao)

# Página principal - estação de trabalho 
@recepcao_bp.route("/<int:setor_id>/<int:estacao_id>/<int:senha_atual_id>/<string:acao>", methods=["GET", "POST"])
@login_required
def senhas(setor_id, estacao_id, senha_atual_id, acao):
    usuario = current_user
    
    setor = obter_setor("id", setor_id)
    
    estacao = obter_estacao("id", estacao_id)
      
    # Senhas relacionadas ao dia atual
    # OBSOLETO: todas_senhas = obter_todas_senhas()
    senhas = obter_senhas_hoje()
    
    senha_json = None 
    
    selecionar_estacao(estacao.id, usuario.id)    # Define a estacao para o usuario atual 
    
    if acao == "senhas_atualizar":
        senhaAtual = obter_senha("id", senha_atual_id)     
        if senhaAtual:
            senha_json = {
                "id": senhaAtual.id,
                "numero": str(senhaAtual.numero).zfill(4),
                "categoria": senhaAtual.categoria,
                "data_hora": senhaAtual.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            }
    
    if acao == "proxima_senha":
        senhaAtual = obter_senha("id", senha_atual_id)
        novaSenha = proxima_senha(setor_id, senha_atual_id)
        
        # Cancela a chamada da senha atual - isso deve ser feito depois de chamado a 'proxima_senha'
        if senhaAtual:
            atualizar_senha_chamada(senhaAtual.id, None, "Aguardando")
        
        if novaSenha:
            # Atualiza 'id_estacao' e 'status'
            atualizar_senha_chamada(novaSenha.id, estacao.id, "Chamando")
            senha_json = {
                "id": novaSenha.id,
                "numero": str(novaSenha.numero).zfill(4),
                "categoria": novaSenha.categoria,
                "data_hora": novaSenha.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            }
            
    if acao == "chamar_novamente":
        senha = obter_senha("id", senha_atual_id)
        if senha:
            # Atualiza o horário da senha pois apenas as 4 últimas são exibidas sendo o destaque para a última
            data_hora_atual = datetime.datetime.now()
            atualizar_hora_senha_chamada(senha.id, data_hora_atual)
            senha_json = {
                "id": senha.id,
                "numero": str(senha.numero).zfill(4),
                "categoria": senha.categoria,
                "data_hora": senha.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            }
    
    if acao == "cancelar_senha":
        senha = obter_senha("id", senha_atual_id)
        if senha:
            atualizar_senha_chamada(senha.id, None, "Aguardando")
            senha_atual_id = 0
    
    if acao == "encerrar_atendimento":
        senha = obter_senha("id", senha_atual_id)
        if senha:
            atualizar_senha_chamada(senha.id, None, "Encerrado")
            senha_atual_id = 0

    #    return redirect(url_for("pacientes.recepcao_criar", usuario = usuario, setor = setor, estacao = estacao))
        #return render_template("paciente/criar.html", usuario = usuario, setor = setor, estacao = estacao) 
    
    senhas_json = [senha.__json__() for senha in senhas if senha.id_setor == setor_id and senha.status == "Aguardando"]

    # request.method == "GET"
    return render_template("recepcao/estacao-recepcao.html", setor = setor, estacao = estacao, senhas = senhas_json, senha_atual = senha_json)

# Rota para atualizar a interface das senhas
@recepcao_bp.route("/auto-refresh")
def auto_refresh():
    id_setor = int(request.args.get("id_setor"))
    id_estacao = int(request.args.get("id_estacao"))
    
    senhas = obter_todas_senhas()
    senhas_aguardando_json = [senha.__json__() for senha in senhas if senha.id_setor == id_setor and senha.status == "Aguardando"]
    
    senha_atual = obter_senha("id_estacao", id_estacao)
    senha_atual_json = None
    if senha_atual:
        senha_atual_json = {
            "id": senha_atual.id,
            "numero": str(senha_atual.numero).zfill(4),
            "categoria": senha_atual.categoria,
            "data_hora": senha_atual.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
    return jsonify(senhas = senhas_aguardando_json, senha_atual = senha_atual_json)

# Seleciona a próxima senha
def proxima_senha(setor_id, senha_atual_id):
    # Versão 1
    # senhas = obter_todas_senhas()
    
    # Versão 2
    senha_atual = obter_senha("id", senha_atual_id)
    senhas = obter_senhas_hoje()
    
    # Primeiro as prioridades
    senhas_prioridade = list(filter(lambda senha: senha.id_setor == setor_id and senha.categoria == "Prioridade" and senha.status == "Aguardando", senhas))
    if senhas_prioridade:
        senhas_ordenadas = sorted(senhas_prioridade, key = lambda s: s.numero, reverse = True)
        # senhas_selecionadas.sort(key=lambda senha: senha.data_hora, reverse=True)
        
        senhas_ordenadas = sorted(senhas_convencionais, key = lambda s: s.numero)
        if senha_atual:
            ultima_senha = senhas_ordenadas[len(senhas_ordenadas) - 1]
            if senha_atual.numero >= ultima_senha.numero:
                ultima_senha = senha_atual
            else:
                for senha in senhas_convencionais:
                    print(f" senhaN = {senha.numero} senha_atual = {senha_atual.numero}")
                    if senha.numero > senha_atual.numero:
                        ultima_senha = senha
                        break
        else:
            ultima_senha = senhas_ordenadas[0]

        
        #ultima_senha = senhas_ordenadas.pop(0)
        # Se a senha for a mesma atual, passa para a próxima
        #if ultima_senha.id == senha_atual_id:
        #    ultima_senha = senhas_ordenadas.pop(0)
            
        return ultima_senha

    # Depois as convencionais
    senhas_convencionais = list(filter(lambda senha: senha.id_setor == setor_id and senha.categoria == "Convencional" and senha.status == "Aguardando", senhas))
    if senhas_convencionais:
        senhas_ordenadas = sorted(senhas_convencionais, key = lambda s: s.numero)
        if senha_atual:
            ultima_senha = senhas_ordenadas[len(senhas_ordenadas) - 1]
            if senha_atual.numero >= ultima_senha.numero:
                ultima_senha = senha_atual
            else:
                for senha in senhas_convencionais:
                    print(f" senhaN = {senha.numero} senha_atual = {senha_atual.numero}")
                    if senha.numero > senha_atual.numero:
                        ultima_senha = senha
                        break
        else:
            ultima_senha = senhas_ordenadas[0]
        
        #ultima_senha = senhas_ordenadas.pop(0)
        # Se a senha for a mesma atual, passa para a próxima
        #if ultima_senha.id == senha_atual_id:
        #    ultima_senha = senhas_ordenadas.pop(0)

        return ultima_senha

    # Nenhuma senha existente
    return None
