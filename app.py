# [Instalação]
# 	python -m venv sga
#	sga\Scripts\activate
#   pip install -r requirements.txt
# Versão de demonstração para toda a rede: 
#   flask run --host=0.0.0.0
# Versão de testes apenas local: 
#   python app.py

# Bibliotecas
import os.path
from flask import Flask
from flask_login import LoginManager
from database import db, create_database, clear_database, db_file_path
from models.usuario import Usuario
from util import set_test_data, erro_internal_server, erro_page_not_found, erro_unautorized
from blueprints import register_blueprints

# Criar e configura o aplicativo Flask
def create_app():
    # Cria o objeto Flask
    app = Flask(__name__)
    
    # Configura o objeto Flask
    app.config.from_pyfile("config.py")
    
    # Configura as páginas de erros
    app.register_error_handler(401, erro_unautorized)
    app.register_error_handler(404, erro_page_not_found)
    app.register_error_handler(404, erro_internal_server)
        
    # Inicializa e configura a extensão Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)   
    @login_manager.user_loader 
    def load_user(usuario_id):
        return db.session.get(Usuario, usuario_id)
    
    # Inicializa a extensção SQLAlchemy
    db.init_app(app)
    
    # Registra os blueprints
    register_blueprints(app)
    
    # Retonar o aplicativo criado
    return app

# Executa o código a seguir se este arquivo for executado diretamente (não como módulo)
if __name__ == "__main__":

    # Cria uma nova aplicação
    app = create_app()

    # Modo desenvolvedor: 
    if os.path.isfile(db_file_path()):  # Banco de dados já criado, reiniciar banco de dados
        print(">>> RESET DATABASE.")
        clear_database(app)
    else:
        print(">>> CREATE DATABASE.")   # Banco de dados não existe ainda, criar banco de dados
        create_database(app)

    # Gera os primeiros registros para testes incluindo usuário 'admin'
    set_test_data(app)

    # Inicializa a aplicação
    app.run()