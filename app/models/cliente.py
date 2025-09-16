from app.extensions import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    contato = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)

    alugueis = db.relationship("Aluguel", back_populates="cliente")