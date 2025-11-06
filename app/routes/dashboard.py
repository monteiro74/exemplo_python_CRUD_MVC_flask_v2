from flask import Blueprint, render_template
from flask_login import login_required
from app.models.aluno import Aluno
from app.models.pet import Pet
from app import db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    """Página principal do dashboard"""

    # Estatísticas
    total_alunos = Aluno.query.count()
    total_pets = Pet.query.count()

    # Dados para gráficos
    alunos_por_curso = db.session.query(
        Aluno.curso,
        db.func.count(Aluno.id)
    ).group_by(Aluno.curso).all()

    alunos_por_sexo = db.session.query(
        Aluno.sexo,
        db.func.count(Aluno.id)
    ).group_by(Aluno.sexo).all()

    # Média de idade
    media_idade = db.session.query(db.func.avg(Aluno.idade)).scalar()
    media_idade = round(media_idade, 1) if media_idade else 0

    # Últimos alunos cadastrados
    ultimos_alunos = Aluno.query.order_by(Aluno.created_at.desc()).limit(5).all()

    return render_template('dashboard/index.html',
                         total_alunos=total_alunos,
                         total_pets=total_pets,
                         media_idade=media_idade,
                         alunos_por_curso=alunos_por_curso,
                         alunos_por_sexo=alunos_por_sexo,
                         ultimos_alunos=ultimos_alunos)
