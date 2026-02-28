from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.cliente import Cliente
from app.models.filme import Filme

class Aluguel(db.Model):
    __tablename__ = 'alugueis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_diaria = db.Column(db.Numeric(10, 2), nullable=False)
    data_aluguel = db.Column(db.DateTime, default=datetime.now)
    data_devolucao_prevista = db.Column(db.DateTime, nullable=False)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    tempo_aluguel = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Boolean, default=True)

    cliente_cpf = db.Column(db.String(11), ForeignKey('clientes.cpf'), nullable=False)
    filme_id = db.Column(db.Integer, ForeignKey('filmes.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="alugueis")
    filme = relationship("Filme", back_populates="alugueis")

    def to_dict(self):
        return {
            "id": self.id,
            "cpf_cliente": self.cliente_cpf,
            "codigo_filme": self.filme_id,
            "data_aluguel": self.data_aluguel.isoformat() if self.data_aluguel else None,
            "data_devolucao_prevista": self.data_devolucao_prevista.isoformat() if self.data_devolucao_prevista else None,
            "data_devolucao": self.data_devolucao.isoformat() if self.data_devolucao else None,
            "tempo_aluguel": self.tempo_aluguel,
            "valor": float(self.valor) if self.valor is not None else None,
            "status": self.status,
            "titulo_filme": self.filme.titulo if self.filme else None
        }