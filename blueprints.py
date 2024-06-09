from routes.auth import auth_bp
from routes.usuarios import usuario_bp
from routes.perfis import perfil_bp
from routes.setores import setor_bp
from routes.estacoes import estacao_bp
from routes.senhas import senha_bp
from routes.recepcao import recepcao_bp

# Registra os Flask-blueprints do sistema
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(setor_bp)
    app.register_blueprint(estacao_bp)
    app.register_blueprint(senha_bp)
    app.register_blueprint(recepcao_bp)