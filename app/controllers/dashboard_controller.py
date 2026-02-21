from datetime import datetime, timedelta

from sqlalchemy import func, case

from app.extensions import db
from app.models.aluguel import Aluguel
from app.models.filme import Filme

DATE_FORMAT = "%Y-%m-%d"


def _date_range(inicio_str=None, fim_str=None):
    hoje = datetime.now().date()
    fim = datetime.strptime(fim_str, DATE_FORMAT).date() if fim_str else hoje
    inicio = datetime.strptime(inicio_str, DATE_FORMAT).date() if inicio_str else fim - timedelta(days=29)

    if inicio > fim:
        inicio, fim = fim, inicio

    inicio_dt = datetime.combine(inicio, datetime.min.time())
    fim_dt = datetime.combine(fim, datetime.max.time())
    return inicio_dt, fim_dt


def _receita_expr():
    return case((Aluguel.valor.isnot(None), Aluguel.valor), else_=Aluguel.valor_diaria)


def obter_resumo(inicio_str=None, fim_str=None):
    inicio, fim = _date_range(inicio_str, fim_str)

    receita_sum = func.sum(_receita_expr())
    total = db.session.query(func.count(Aluguel.id)).filter(
        Aluguel.data_aluguel.between(inicio, fim)
    ).scalar() or 0

    receita = db.session.query(receita_sum).filter(
        Aluguel.data_aluguel.between(inicio, fim)
    ).scalar() or 0.0

    ticket = float(receita) / total if total else 0.0

    return {
        "periodo": {
            "inicio": inicio.date().isoformat(),
            "fim": fim.date().isoformat()
        },
        "total_alugueis": int(total),
        "receita_total": float(round(receita, 2)),
        "ticket_medio": float(round(ticket, 2))
    }


def obter_series(inicio_str=None, fim_str=None):
    inicio, fim = _date_range(inicio_str, fim_str)
    receita_sum = func.sum(_receita_expr())
    dia_expr = func.date(Aluguel.data_aluguel)

    rows = (
        db.session.query(
            dia_expr.label("dia"),
            func.count(Aluguel.id).label("total"),
            receita_sum.label("receita")
        )
        .filter(Aluguel.data_aluguel.between(inicio, fim))
        .group_by(dia_expr)
        .order_by(dia_expr)
        .all()
    )

    return [
        {
            "data": row.dia.isoformat() if hasattr(row.dia, "isoformat") else str(row.dia),
            "total_alugueis": int(row.total or 0),
            "receita": float(round((row.receita or 0.0), 2))
        }
        for row in rows
    ]


def obter_status(inicio_str=None, fim_str=None):
    inicio, fim = _date_range(inicio_str, fim_str)

    ativos_case = func.sum(case((Aluguel.status.is_(True), 1), else_=0))
    finalizados_case = func.sum(case((Aluguel.status.is_(False), 1), else_=0))

    ativos, finalizados = (
        db.session.query(ativos_case, finalizados_case)
        .filter(Aluguel.data_aluguel.between(inicio, fim))
        .one()
    )

    ativos = int(ativos or 0)
    finalizados = int(finalizados or 0)
    total = ativos + finalizados

    percentual_ativos = round((ativos / total) * 100, 2) if total else 0.0
    percentual_finalizados = round(100 - percentual_ativos, 2) if total else 0.0

    return {
        "ativos": ativos,
        "finalizados": finalizados,
        "percentuais": {
            "ativos": percentual_ativos,
            "finalizados": percentual_finalizados
        }
    }


def obter_top_filmes(inicio_str=None, fim_str=None, limite=5):
    inicio, fim = _date_range(inicio_str, fim_str)
    limite = max(1, min(int(limite or 5), 10))

    rows = (
        db.session.query(
            Filme.titulo.label("titulo"),
            func.count(Aluguel.id).label("total")
        )
        .join(Filme, Filme.id == Aluguel.filme_id)
        .filter(Aluguel.data_aluguel.between(inicio, fim))
        .group_by(Filme.titulo)
        .order_by(func.count(Aluguel.id).desc())
        .limit(limite)
        .all()
    )

    return [
        {
            "titulo": row.titulo or "N/D",
            "total_alugueis": int(row.total or 0)
        }
        for row in rows
    ]


def obter_top_generos(inicio_str=None, fim_str=None, limite=5):
    inicio, fim = _date_range(inicio_str, fim_str)
    limite = max(1, min(int(limite or 5), 10))

    rows = (
        db.session.query(
            Filme.genero.label("genero"),
            func.count(Aluguel.id).label("total")
        )
        .join(Filme, Filme.id == Aluguel.filme_id)
        .filter(Aluguel.data_aluguel.between(inicio, fim))
        .group_by(Filme.genero)
        .order_by(func.count(Aluguel.id).desc())
        .limit(limite)
        .all()
    )

    return [
        {
            "genero": row.genero or "N/D",
            "total_alugueis": int(row.total or 0)
        }
        for row in rows
    ]
