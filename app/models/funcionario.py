from app.extensions import db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(60), nullable=False)
    contato = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "cargo": self.cargo,
            "contato": self.contato,
            "endereco": self.endereco
        }


