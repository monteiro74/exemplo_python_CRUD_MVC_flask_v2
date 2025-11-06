# Importar todos os blueprints
from app.routes.auth import bp as auth_bp
from app.routes.dashboard import bp as dashboard_bp
from app.routes.alunos import bp as alunos_bp
from app.routes.pets import bp as pets_bp
from app.routes.relatorios import bp as relatorios_bp

__all__ = ['auth_bp', 'dashboard_bp', 'alunos_bp', 'pets_bp', 'relatorios_bp']
