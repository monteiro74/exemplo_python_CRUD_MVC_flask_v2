from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models.pet import Pet
from app.models.aluno import Aluno
from datetime import datetime

bp = Blueprint('pets', __name__, url_prefix='/pets')

@bp.route('/')
@login_required
def index():
    """Lista todos os pets"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Busca
    search = request.args.get('search', '')
    query = Pet.query.join(Aluno)

    if search:
        query = query.filter(
            db.or_(
                Pet.apelido.like(f'%{search}%'),
                Pet.raca.like(f'%{search}%'),
                Aluno.nome.like(f'%{search}%')
            )
        )

    pets = query.order_by(Pet.apelido).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('pets/index.html', pets=pets, search=search)

@bp.route('/criar', methods=['GET', 'POST'])
@login_required
def criar():
    """Criar novo pet"""
    if request.method == 'POST':
        apelido = request.form.get('apelido')
        raca = request.form.get('raca')
        data_nascimento = request.form.get('data_nascimento')
        aluno_id = request.form.get('aluno_id')

        # Validações
        if not apelido or not aluno_id:
            flash('Apelido e dono são obrigatórios.', 'danger')
            return redirect(url_for('pets.criar'))

        # Verificar se aluno existe
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            flash('Aluno não encontrado.', 'danger')
            return redirect(url_for('pets.criar'))

        # Criar pet
        pet = Pet(
            apelido=apelido,
            raca=raca,
            aluno_id=aluno_id
        )

        if data_nascimento:
            try:
                pet.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                flash('Data de nascimento inválida.', 'danger')
                return redirect(url_for('pets.criar'))

        db.session.add(pet)
        db.session.commit()

        flash(f'Pet {apelido} cadastrado com sucesso!', 'success')
        return redirect(url_for('pets.index'))

    alunos = Aluno.query.order_by(Aluno.nome).all()
    return render_template('pets/form.html', pet=None, alunos=alunos)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar pet existente"""
    pet = Pet.query.get_or_404(id)

    if request.method == 'POST':
        apelido = request.form.get('apelido')
        raca = request.form.get('raca')
        data_nascimento = request.form.get('data_nascimento')
        aluno_id = request.form.get('aluno_id')

        # Validações
        if not apelido or not aluno_id:
            flash('Apelido e dono são obrigatórios.', 'danger')
            return redirect(url_for('pets.editar', id=id))

        # Verificar se aluno existe
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            flash('Aluno não encontrado.', 'danger')
            return redirect(url_for('pets.editar', id=id))

        # Atualizar dados
        pet.apelido = apelido
        pet.raca = raca
        pet.aluno_id = aluno_id

        if data_nascimento:
            try:
                pet.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                flash('Data de nascimento inválida.', 'danger')
                return redirect(url_for('pets.editar', id=id))

        db.session.commit()

        flash(f'Pet {apelido} atualizado com sucesso!', 'success')
        return redirect(url_for('pets.index'))

    alunos = Aluno.query.order_by(Aluno.nome).all()
    return render_template('pets/form.html', pet=pet, alunos=alunos)

@bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    """Excluir pet"""
    pet = Pet.query.get_or_404(id)
    apelido = pet.apelido

    db.session.delete(pet)
    db.session.commit()

    flash(f'Pet {apelido} excluído com sucesso!', 'success')
    return redirect(url_for('pets.index'))

@bp.route('/api/por-aluno/<int:aluno_id>')
@login_required
def api_por_aluno(aluno_id):
    """API: Retorna pets de um aluno específico"""
    pets = Pet.query.filter_by(aluno_id=aluno_id).all()
    data = [pet.to_dict() for pet in pets]
    return jsonify(data)

@bp.route('/api/exportar')
@login_required
def exportar():
    """Exportar dados dos pets em JSON"""
    pets = Pet.query.all()
    data = [pet.to_dict() for pet in pets]
    return jsonify(data)
