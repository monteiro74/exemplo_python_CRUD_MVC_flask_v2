from app import db
from datetime import datetime

class Aluno(db.Model):
    """Modelo de Aluno"""
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    curso = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(1))  # M ou F
    foto = db.Column(db.LargeBinary)  # BLOB para armazenar imagem
    foto_filename = db.Column(db.String(255))  # Nome do arquivo da foto
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com pets
    pets = db.relationship('Pet', backref='dono', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Aluno {self.matricula} - {self.nome}>'

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'matricula': self.matricula,
            'nome': self.nome,
            'curso': self.curso,
            'idade': self.idade,
            'sexo': self.sexo,
            'foto_filename': self.foto_filename,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M') if self.updated_at else None
        }
