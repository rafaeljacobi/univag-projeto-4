from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models.perfil import Perfil, obter_id_perfil
from models.usuario import Usuario
from models.setor import Setor
from models.estacao import Estacao
from database import CRUD

# Cria os primeiros dados para testes
def set_test_data(app):
    with app.app_context(): 
        crud_setor = CRUD(Setor)       
        crud_setor.create({"descricao": "Recepção"})
        crud_setor.create({"descricao": "Entrega de Exames"})
        
        crud_perfil = CRUD(Perfil)
        crud_perfil.create({"descricao": "Administrador"})
        crud_perfil.create({"descricao": "Recepcionista"})
        
        crud_estacao = CRUD(Estacao)
        crud_estacao.create({"descricao": "Guiche 1", "id_setor": 1})
        crud_estacao.create({"descricao": "Guiche 2", "id_setor": 1})
        crud_estacao.create({"descricao": "Guiche 1", "id_setor": 2})
               
        crud_admin = CRUD(Usuario)       
        id_perfil = obter_id_perfil("Administrador")
        crud_admin.create({"nome": "admin", "email": "admin@admin", "senha": criar_senha("123"), "id_perfil": id_perfil})
        print(">>> CREATE ADMIN.")
        id_perfil = obter_id_perfil("Recepcionista")
        crud_admin.create({"nome": "teste", "email": "teste@teste", "senha": criar_senha("123"), "id_perfil": id_perfil})
        
# Criptografia para as senhas - TODO: melhorar a abordagem
def conferir_senha(senha_armazenada, senha_digitada):
    return check_password_hash(senha_armazenada, senha_digitada)

def criar_senha(senha_digitada):
    return generate_password_hash(senha_digitada)

# Página para erro 401 - não autorizado
def erro_unautorized(e):
    return render_template("erros/401.html"), 401

# Página para erro 404 - página não existe
def erro_page_not_found(e):
    return render_template("erros/404.html"), 404

# Página para erro 500 - erro interno do servidor
def erro_internal_server(e):
    return render_template("erros/501.html"), 501