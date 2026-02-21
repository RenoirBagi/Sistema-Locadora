from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.cliente import Cliente
from app.models.filme import Filme

class Aluguel(db.Model):
    __tablename__ = 'alugueis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_diaria = db.Column(db.Float, nullable=False)
    data_aluguel = db.Column(db.DateTime, default=datetime.now)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    tempo_aluguel = db.Column(db.Integer, nullable=True)
    valor = db.Column(db.Float, nullable=True)
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
            "data_devolucao": self.data_devolucao.isoformat() if self.data_devolucao else None,
            "valor": self.valor,
            "status": self.status
            # Opcional: incluir nomes para facilitar no frontend sem fetch extra
            # "nome_cliente": self.cliente.nome if self.cliente else None,
            # "titulo_filme": self.filme.titulo if self.filme else None
        }