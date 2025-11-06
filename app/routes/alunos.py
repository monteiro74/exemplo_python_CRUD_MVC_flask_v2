from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required
from app import db
from app.models.aluno import Aluno
from werkzeug.utils import secure_filename
import os
from io import BytesIO

bp = Blueprint('alunos', __name__, url_prefix='/alunos')

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def index():
    """Lista todos os alunos"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Busca
    search = request.args.get('search', '')
    query = Aluno.query

    if search:
        query = query.filter(
            db.or_(
                Aluno.nome.like(f'%{search}%'),
                Aluno.matricula.like(f'%{search}%'),
                Aluno.curso.like(f'%{search}%')
            )
        )

    alunos = query.order_by(Aluno.nome).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('alunos/index.html', alunos=alunos, search=search)

@bp.route('/criar', methods=['GET', 'POST'])
@login_required
def criar():
    """Criar novo aluno"""
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        nome = request.form.get('nome')
        curso = request.form.get('curso')
        idade = request.form.get('idade')
        sexo = request.form.get('sexo')

        # Validações
        if not matricula or not nome:
            flash('Matrícula e nome são obrigatórios.', 'danger')
            return redirect(url_for('alunos.criar'))

        if Aluno.query.filter_by(matricula=matricula).first():
            flash('Matrícula já cadastrada.', 'danger')
            return redirect(url_for('alunos.criar'))

        # Criar aluno
        aluno = Aluno(
            matricula=matricula,
            nome=nome,
            curso=curso,
            idade=int(idade) if idade else None,
            sexo=sexo
        )

        # Processar foto
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                aluno.foto = file.read()
                aluno.foto_filename = filename

        db.session.add(aluno)
        db.session.commit()

        flash(f'Aluno {nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('alunos.index'))

    return render_template('alunos/form.html', aluno=None)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar aluno existente"""
    aluno = Aluno.query.get_or_404(id)

    if request.method == 'POST':
        matricula = request.form.get('matricula')
        nome = request.form.get('nome')
        curso = request.form.get('curso')
        idade = request.form.get('idade')
        sexo = request.form.get('sexo')

        # Validações
        if not matricula or not nome:
            flash('Matrícula e nome são obrigatórios.', 'danger')
            return redirect(url_for('alunos.editar', id=id))

        # Verificar matrícula duplicada
        existing = Aluno.query.filter_by(matricula=matricula).first()
        if existing and existing.id != id:
            flash('Matrícula já cadastrada para outro aluno.', 'danger')
            return redirect(url_for('alunos.editar', id=id))

        # Atualizar dados
        aluno.matricula = matricula
        aluno.nome = nome
        aluno.curso = curso
        aluno.idade = int(idade) if idade else None
        aluno.sexo = sexo

        # Processar foto
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                aluno.foto = file.read()
                aluno.foto_filename = filename

        db.session.commit()

        flash(f'Aluno {nome} atualizado com sucesso!', 'success')
        return redirect(url_for('alunos.index'))

    return render_template('alunos/form.html', aluno=aluno)

@bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    """Excluir aluno"""
    aluno = Aluno.query.get_or_404(id)
    nome = aluno.nome

    db.session.delete(aluno)
    db.session.commit()

    flash(f'Aluno {nome} excluído com sucesso!', 'success')
    return redirect(url_for('alunos.index'))

@bp.route('/foto/<int:id>')
@login_required
def foto(id):
    """Retorna a foto do aluno"""
    aluno = Aluno.query.get_or_404(id)

    if not aluno.foto:
        # Retornar imagem padrão
        return redirect(url_for('static', filename='img/no-photo.png'))

    return send_file(
        BytesIO(aluno.foto),
        mimetype='image/jpeg',
        as_attachment=False,
        download_name=aluno.foto_filename or 'foto.jpg'
    )

@bp.route('/detalhes/<int:id>')
@login_required
def detalhes(id):
    """Visualizar detalhes do aluno"""
    aluno = Aluno.query.get_or_404(id)
    return render_template('alunos/detalhes.html', aluno=aluno)

@bp.route('/api/exportar')
@login_required
def exportar():
    """Exportar dados dos alunos em JSON"""
    alunos = Aluno.query.all()
    data = [aluno.to_dict() for aluno in alunos]
    return jsonify(data)
