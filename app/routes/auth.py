from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            remember = request.form.get('remember', False)

            # Debug
            print(f"\n{'='*60}")
            print(f"DEBUG - Tentativa de login: username='{username}'")
            print(f"{'='*60}")

            user = User.query.filter_by(username=username).first()

            # Debug
            if user:
                print(f"DEBUG - Usuário encontrado: {user.username}")
                print(f"DEBUG - Email: {user.email}")
                print(f"DEBUG - Ativo: {user.ativo}")
                print(f"DEBUG - Hash presente: {bool(user.password_hash)}")

                print(f"DEBUG - Verificando senha...")
                senha_valida = user.check_password(password)
                print(f"DEBUG - Senha válida: {senha_valida}")
            else:
                print(f"DEBUG - Usuário '{username}' NÃO encontrado no banco!")

            if user and user.check_password(password):
                print(f"DEBUG - Autenticação OK! Verificando se está ativo...")

                if not user.ativo:
                    print(f"DEBUG - Usuário INATIVO!")
                    flash('Sua conta está desativada. Contate o administrador.', 'danger')
                    return redirect(url_for('auth.login'))

                print(f"DEBUG - Atualizando último login...")
                # Atualizar último login
                user.last_login = datetime.utcnow()
                db.session.commit()

                print(f"DEBUG - Fazendo login do usuário...")
                login_user(user, remember=remember)
                print(f"DEBUG - Login efetuado com sucesso!")

                flash(f'Bem-vindo, {user.nome_completo or user.username}!', 'success')

                # Redirecionar para página solicitada ou dashboard
                next_page = request.args.get('next')
                print(f"DEBUG - Redirecionando para dashboard...")
                return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
            else:
                if not user:
                    print(f"DEBUG - FALHA: Usuário não encontrado")
                    flash('Usuário não encontrado.', 'danger')
                else:
                    print(f"DEBUG - FALHA: Senha incorreta")
                    flash('Senha incorreta.', 'danger')

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"ERRO DURANTE LOGIN: {str(e)}")
            print(f"{'='*60}\n")
            import traceback
            traceback.print_exc()
            flash('Erro ao processar login. Tente novamente.', 'danger')

    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de novo usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        nome_completo = request.form.get('nome_completo')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Validações
        if not all([username, email, password, password_confirm]):
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('auth.register'))

        if password != password_confirm:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('auth.register'))

        # Criar novo usuário
        user = User(username=username, email=email, nome_completo=nome_completo)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
