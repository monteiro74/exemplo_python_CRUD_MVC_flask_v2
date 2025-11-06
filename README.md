# exemplo_python_CRUD_MVC_flask
CRUD_MVC com FLASK


✅ Estrutura Completa
flask_app/
├── app/                      # Aplicação principal<br>
│   ├── models/              # User, Aluno, Pet (SQLAlchemy)<br>
│   ├── routes/              # Blueprints (auth, dashboard, alunos, pets, relatorios)<br>
│   ├── templates/           # HTML com Jinja2<br>
│   └── static/              # CSS, JS, uploads<br>
├── config.py                # Configurações<br>
├── run.py                   # Script principal<br>
├── requirements.txt         # Dependências<br>
└── README.md               # Documentação completa<br>

🎯 Funcionalidades Implementadas

✅ Autenticação

* Login e registro
* Flask-Login
* Senhas hasheadas

✅ Dashboard

* Estatísticas em tempo real
* Gráficos Chart.js
* Cards informativos

✅ CRUD Alunos

* Formulários completos
* Upload de fotos (BLOB)
* Busca e paginação

✅ CRUD Pets

* Relacionamento com alunos
* Mestre-detalhe

✅ Relatórios

* PDF dinâmico (fpdf2)
* Gráficos estatísticos
* Exportação JSON
* Relatório mestre-detalhe

✅ Interface Moderna

* Bootstrap 5 
* Design responsivo
* Icons e animações

🚀 Como Usar:

Instalar dependências:

cd flask_app<br>
python -m venv venv<br>
venv\Scripts\activate  # Windows<br>
pip install -r requirements.txt<br>

Configurar .env:<br>
cp .env.example .env<br>

# Editar com suas configurações de banco

Inicializar:

flask init-db<br>
flask create-admin<br>
flask seed-db  # (opcional)<br>

Executar:

python run.py


📝 Características Especiais:

Arquitetura MVC organizada<br>
Blueprints modulares<br>
SQLAlchemy ORM para banco de dados<br>
Migrations com Flask-Migrate<br>
Segurança com hash de senhas<br>
Uploads de imagens em BLOB<br>
Gráficos interativos com Chart.js<br>
PDF gerados dinamicamente<br>
API REST para exportação JSON<br>
Responsivo para mobile<br>

🔧 Como Configurar:

Copie o arquivo de exemplo:

cd flask_app<br>
copy .env.example .env<br>
Edite o arquivo .env com suas configurações:<br>

# Configurações do Flask

FLASK_APP=run.py<br>
FLASK_ENV=development<br>
SECRET_KEY=sua-chave-secreta-mude-em-producao<br>

# Configurações do Banco de Dados MySQL/MariaDB

DB_HOST=localhost<br>
DB_PORT=3306<br>
DB_NAME=escola_db<br>
DB_USER=admin_exemplo<br>
DB_PASSWORD=sua-senha-aqui<br>

# Configurações de Upload

UPLOAD_FOLDER=app/static/uploads<br>
MAX_CONTENT_LENGTH=16777216<br>
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif<br>

🔄 Como Funciona:

O arquivo config.py lê essas variáveis do .env:

DB_HOST = os.environ.get('DB_HOST', 'localhost')<br>
DB_PORT = os.environ.get('DB_PORT', '3306')<br>
DB_NAME = os.environ.get('DB_NAME', 'escola_db')
DB_USER = os.environ.get('DB_USER', 'admin_exemplo')<br>
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'sua-senha-aqui')<br>

SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

⚠️ Importante:<br>
⚠️ Nunca commite o arquivo .env no Git (já está no .gitignore)<br>


Use .env.example como template<br>
Crie o banco de dados antes:<br>

CREATE DATABASE escola_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

📝 Exemplo Completo:

Se você estiver usando Laragon com MariaDB:

DB_HOST=localhost<br>
DB_PORT=3306<br>
DB_NAME=escola_db<br>
DB_USER=admin_exemplo<br>
DB_PASSWORD=sua-senha-aqui<br>

Solução:

1. Criar e ativar ambiente virtual:

cd flask_app<br>
python -m venv venv<br>
Ativar o ambiente virtual:<br>
# Windows<br>
venv\Scripts\activate<br>

# Você verá (venv) no início da linha de comando

2. Instalar as dependências:

pip install -r requirements.txt

3. Verificar instalação:

pip list<br>

Você deve ver pacotes como:

Flask<br>
Flask-SQLAlchemy<br>
Flask-Login<br>
Flask-Migrate<br>
mysql-connector-python<br>
etc.<br>

4. Agora execute novamente:

python run.py
