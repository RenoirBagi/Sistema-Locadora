from app.extensions import db

class Filme(db.Model):
    __tablename__ = 'filmes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

    alugueis = db.relationship('Aluguel', back_populates='filme')

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "ano": self.ano,
            "preco": float(self.preco) if self.preco is not None else None,
            "disponivel": self.disponivel
        }