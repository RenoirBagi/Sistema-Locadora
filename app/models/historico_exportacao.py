from datetime import datetime

from app.extensions import db


class HistoricoExportacao(db.Model): 
    __tablename__ = 'historico_exportacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_relatorio = db.Column(db.String(20), nullable=False)
    formato = db.Column(db.String(5), nullable=False)
    periodo_inicio = db.Column(db.DateTime, nullable=False)
    periodo_fim = db.Column(db.DateTime, nullable=False)
    total_registros = db.Column(db.Integer, nullable=False, default=0)
    tamanho_bytes = db.Column(db.BigInteger, nullable=False, default=0)
    status = db.Column(db.String(10), nullable=False, default='sucesso')
    mensagem_erro = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_relatorio': self.tipo_relatorio,
            'formato': self.formato,
            'periodo_inicio': self.periodo_inicio.isoformat(),
            'periodo_fim': self.periodo_fim.isoformat(),
            'total_registros': self.total_registros,
            'status': self.status,
            'tamanho_bytes': self.tamanho_bytes,
            'mensagem_erro': self.mensagem_erro,
            'criado_em': self.criado_em.isoformat()
        }
