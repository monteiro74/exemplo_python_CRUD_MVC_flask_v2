from app import db
from datetime import datetime

class Pet(db.Model):
    """Modelo de Pet"""
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    apelido = db.Column(db.String(100), nullable=False)
    raca = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Pet {self.apelido} - {self.raca}>'

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'apelido': self.apelido,
            'raca': self.raca,
            'data_nascimento': self.data_nascimento.strftime('%d/%m/%Y') if self.data_nascimento else None,
            'aluno_id': self.aluno_id,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M') if self.updated_at else None
        }
