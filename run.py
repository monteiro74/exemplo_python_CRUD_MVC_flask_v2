#!/usr/bin/env python
"""
Script principal para executar a aplicação Flask
"""
import os
from app import create_app, db
from app.models import User, Aluno, Pet

# Criar instância da aplicação
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Adiciona objetos ao shell context para facilitar testes"""
    return {
        'db': db,
        'User': User,
        'Aluno': Aluno,
        'Pet': Pet
    }

@app.cli.command()
def init_db():
    """Inicializa o banco de dados"""
    db.create_all()
    print('Banco de dados inicializado!')

@app.cli.command()
def create_admin():
    """Cria um usuário administrador padrão"""
    from app.models.user import User

    # Verificar se já existe
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('Usuário admin já existe!')
        return

    # Criar novo admin
    admin = User(
        username='admin',
        email='admin@escola.com',
        nome_completo='Administrador do Sistema'
    )
    admin.set_password('admin123')

    db.session.add(admin)
    db.session.commit()

    print('Usuário admin criado com sucesso!')
    print('Username: admin')
    print('Password: admin123')
    print('IMPORTANTE: Altere a senha após o primeiro login!')

@app.cli.command()
def seed_db():
    """Popula o banco com dados de exemplo"""
    from app.models.aluno import Aluno
    from app.models.pet import Pet
    from datetime import date

    print('Populando banco de dados...')

    # Criar alunos de exemplo
    alunos_exemplo = [
        Aluno(matricula='2024001', nome='João Silva', curso='Engenharia', idade=20, sexo='M'),
        Aluno(matricula='2024002', nome='Maria Santos', curso='Medicina', idade=22, sexo='F'),
        Aluno(matricula='2024003', nome='Pedro Oliveira', curso='Direito', idade=21, sexo='M'),
        Aluno(matricula='2024004', nome='Ana Costa', curso='Arquitetura', idade=23, sexo='F'),
        Aluno(matricula='2024005', nome='Carlos Souza', curso='Engenharia', idade=19, sexo='M'),
    ]

    for aluno in alunos_exemplo:
        db.session.add(aluno)

    db.session.commit()
    print(f'{len(alunos_exemplo)} alunos criados!')

    # Criar pets de exemplo
    pets_exemplo = [
        Pet(apelido='Rex', raca='Labrador', data_nascimento=date(2020, 5, 15), aluno_id=1),
        Pet(apelido='Mimi', raca='Siamês', data_nascimento=date(2021, 3, 20), aluno_id=2),
        Pet(apelido='Bob', raca='Bulldog', data_nascimento=date(2019, 8, 10), aluno_id=3),
        Pet(apelido='Luna', raca='Golden Retriever', data_nascimento=date(2020, 12, 5), aluno_id=4),
    ]

    for pet in pets_exemplo:
        db.session.add(pet)

    db.session.commit()
    print(f'{len(pets_exemplo)} pets criados!')
    print('Banco de dados populado com sucesso!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
