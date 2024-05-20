# Versão de demonstração para toda a rede: 
# flask run --host=0.0.0.0
# Versão de testes apenas local: 
# python app.py

import os.path
from flask import Flask
from flask_login import LoginManager
from database import db, create_database, clear_database, db_file_path
from models.usuario import Usuario
from routes.auth import auth_bp
from routes.usuarios import usuario_bp
from routes.perfis import perfil_bp
from routes.setores import setor_bp
from routes.estacoes import estacao_bp
from routes.senhas import senha_bp
from routes.recepcao import recepcao_bp
from util import set_test_data

def create_app():
    # Cria a aplicação Flask
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    
    # Configura o Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)   
    @login_manager.user_loader 
    def load_user(usuario_id):
        return db.session.get(Usuario, usuario_id)
    
    # Inicializad o SQLAlchemy
    db.init_app(app)
    
    # Registra os blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(setor_bp)
    app.register_blueprint(estacao_bp)
    app.register_blueprint(senha_bp)
    app.register_blueprint(recepcao_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    if os.path.isfile(db_file_path()):  # Banco de dados já criado
        print(">>> RESET DATABASE.")
        clear_database(app)
    else:
        print(">>> CREATE DATABASE.")   # Banco de dados não existe ainda
        create_database(app)
    set_test_data(app)
    app.run()