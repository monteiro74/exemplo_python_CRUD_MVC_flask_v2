from flask import Blueprint, render_template, send_file, request
from flask_login import login_required
from app.models.aluno import Aluno
from app.models.pet import Pet
from app import db
from fpdf import FPDF
import io
from datetime import datetime

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@bp.route('/')
@login_required
def index():
    """Página de relatórios"""
    return render_template('relatorios/index.html')

@bp.route('/alunos-pdf')
@login_required
def alunos_pdf():
    """Gera relatório PDF de alunos"""

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Relatório de Alunos', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 5, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    # Cabeçalho da tabela
    pdf.cell(30, 10, 'Matrícula', 1)
    pdf.cell(70, 10, 'Nome', 1)
    pdf.cell(50, 10, 'Curso', 1)
    pdf.cell(20, 10, 'Idade', 1)
    pdf.cell(20, 10, 'Sexo', 1)
    pdf.ln()

    # Dados
    pdf.set_font('Arial', '', 10)
    alunos = Aluno.query.order_by(Aluno.nome).all()

    for aluno in alunos:
        pdf.cell(30, 8, aluno.matricula or '', 1)
        pdf.cell(70, 8, aluno.nome[:30] if aluno.nome else '', 1)
        pdf.cell(50, 8, aluno.curso[:20] if aluno.curso else '', 1)
        pdf.cell(20, 8, str(aluno.idade) if aluno.idade else '', 1, 0, 'C')
        pdf.cell(20, 8, aluno.sexo or '', 1, 0, 'C')
        pdf.ln()

    # Total
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, f'Total de alunos: {len(alunos)}', 0, 1)

    # Retornar PDF
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'relatorio_alunos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@bp.route('/estatisticas')
@login_required
def estatisticas():
    """Página de estatísticas e gráficos"""

    # Alunos por curso
    alunos_por_curso = db.session.query(
        Aluno.curso,
        db.func.count(Aluno.id).label('total')
    ).group_by(Aluno.curso).all()

    # Alunos por sexo
    alunos_por_sexo = db.session.query(
        Aluno.sexo,
        db.func.count(Aluno.id).label('total')
    ).group_by(Aluno.sexo).all()

    # Distribuição de idade
    distribuicao_idade = db.session.query(
        db.case(
            (Aluno.idade < 18, 'Menor de 18'),
            (Aluno.idade.between(18, 25), '18-25'),
            (Aluno.idade.between(26, 35), '26-35'),
            (Aluno.idade > 35, 'Maior de 35')
        ).label('faixa'),
        db.func.count(Aluno.id).label('total')
    ).filter(Aluno.idade.isnot(None)).group_by('faixa').all()

    # Pets por raça
    pets_por_raca = db.session.query(
        Pet.raca,
        db.func.count(Pet.id).label('total')
    ).group_by(Pet.raca).limit(10).all()

    return render_template('relatorios/estatisticas.html',
                         alunos_por_curso=alunos_por_curso,
                         alunos_por_sexo=alunos_por_sexo,
                         distribuicao_idade=distribuicao_idade,
                         pets_por_raca=pets_por_raca)

@bp.route('/mestre-detalhe')
@login_required
def mestre_detalhe():
    """Relatório mestre-detalhe: Alunos e seus pets"""
    aluno_id = request.args.get('aluno_id', type=int)

    if aluno_id:
        aluno = Aluno.query.get_or_404(aluno_id)
        alunos = [aluno]
    else:
        alunos = Aluno.query.order_by(Aluno.nome).all()

    return render_template('relatorios/mestre_detalhe.html', alunos=alunos)
