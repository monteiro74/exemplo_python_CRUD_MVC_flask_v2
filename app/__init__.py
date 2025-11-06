from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Inicializar extensões
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='default'):
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)

    # Carregar configurações
    from config import config
    app.config.from_object(config[config_name])

    # Garantir que pastas necessárias existam
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'logs'), exist_ok=True)

    # Inicializar extensões com a app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configurações do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Importar e registrar blueprints
    from app.routes import auth, dashboard, alunos, pets, relatorios

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(alunos.bp)
    app.register_blueprint(pets.bp)
    app.register_blueprint(relatorios.bp)

    # User loader para Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Contexto de template global
    @app.context_processor
    def utility_processor():
        def format_date(date):
            if date:
                return date.strftime('%d/%m/%Y')
            return ''
        return dict(format_date=format_date)

    # Criar tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app
