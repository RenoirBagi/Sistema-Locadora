from datetime import datetime
from io import BytesIO

import pandas as pd
from sqlalchemy import func

from app.extensions import db
from app.models.aluguel import Aluguel
from app.models.cliente import Cliente
from app.models.filme import Filme
from app.models.historico_exportacao import HistoricoExportacao
from app.utils import get_date_range


def _dados_alugueis(inicio, fim):
    rows = (
        db.session.query(
            Aluguel.id.label('id_aluguel'),
            Aluguel.data_aluguel,
            Aluguel.data_devolucao,
            Aluguel.status,
            Cliente.cpf.label('cliente_cpf'),
            Cliente.nome.label('cliente_nome'),
            Filme.id.label('filme_id'),
            Filme.titulo.label('filme_titulo'),
            Aluguel.valor_diaria,
            func.coalesce(Aluguel.valor, Aluguel.valor_diaria).label('valor_total')
        )
        .join(Cliente, Cliente.cpf == Aluguel.cliente_cpf)
        .join(Filme, Filme.id == Aluguel.filme_id)
        .filter(Aluguel.data_aluguel.between(inicio, fim))
        .order_by(Aluguel.data_aluguel)
        .all()
    )

    dados = []
    for row in rows:
        dados.append({
            'ID Aluguel': row.id_aluguel,
            'Data Aluguel': row.data_aluguel.strftime('%d/%m/%Y') if row.data_aluguel else '',
            'Data Devolução Prevista': row.data_devolucao.strftime('%d/%m/%Y') if row.data_devolucao else '',
            'Status': 'Ativo' if row.status else 'Finalizado',
            'CPF Cliente': row.cliente_cpf,
            'Nome Cliente': row.cliente_nome,
            'ID Filme': row.filme_id,
            'Título Filme': row.filme_titulo,
            'Valor Diária': round(row.valor_diaria or 0, 2),
            'Valor Total (estimado)': round(row.valor_total or 0, 2)
        })
    return dados


def _dados_filmes(inicio, fim):
    receita_expr = func.coalesce(Aluguel.valor, Aluguel.valor_diaria, 0)
    rows = (
        db.session.query(
            Filme.id,
            Filme.titulo,
            Filme.genero,
            Filme.ano,
            Filme.preco,
            func.count(Aluguel.id).label('total_alugueis'),
            func.coalesce(func.sum(receita_expr), 0).label('receita')
        )
        .outerjoin(
            Aluguel,
            (Aluguel.filme_id == Filme.id) & (Aluguel.data_aluguel.between(inicio, fim))
        )
        .group_by(Filme.id)
        .order_by(func.count(Aluguel.id).desc(), Filme.titulo)
        .all()
    )

    dados = []
    for row in rows:
        dados.append({
            'ID Filme': row.id,
            'Título': row.titulo,
            'Gênero': row.genero,
            'Ano': row.ano,
            'Valor/Diária': round(row.preco or 0, 2),
            'Total de Aluguéis': int(row.total_alugueis or 0),
            'Receita no Período': round(row.receita or 0, 2)
        })
    return dados


def _gerar_planilha(dados, formato, tipo, inicio, fim):
    df = pd.DataFrame(dados)
    if df.empty:
        df = pd.DataFrame({'Aviso': ['Nenhum registro para o período selecionado']})

    filename = f"{tipo.replace(' ', '_')}_{inicio.date()}_{fim.date()}.{formato}"

    if formato == 'csv':
        conteudo = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
        buffer = BytesIO(conteudo.encode('utf-8-sig'))
        mimetype = 'text/csv'
    else:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatório', index=False)
        buffer.seek(0)
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    buffer.seek(0)
    return buffer, mimetype, filename


def gerar_exportacao(tipo, formato, inicio_str, fim_str):
    tipo = (tipo or '').lower()
    formato = (formato or '').lower()
    if tipo not in {'aluguéis', 'alugueis', 'filmes'}:
        raise ValueError('Tipo de relatório inválido')
    if formato not in {'csv', 'xlsx'}:
        raise ValueError('Formato inválido')

    inicio, fim = get_date_range(inicio_str, fim_str, days_back=0)
    tipo_padrao = 'aluguéis' if tipo in {'aluguéis', 'alugueis'} else 'filmes'

    dados = _dados_alugueis(inicio, fim) if tipo_padrao == 'aluguéis' else _dados_filmes(inicio, fim)
    buffer, mimetype, filename = _gerar_planilha(dados, formato, tipo_padrao, inicio, fim)
    buffer.seek(0)

    return {
        'buffer': buffer,
        'mimetype': mimetype,
        'filename': filename,
        'tipo_relatorio': tipo_padrao,
        'inicio': inicio,
        'fim': fim,
        'total_registros': len(dados),
        'tamanho_bytes': buffer.getbuffer().nbytes
    }


def registrar_historico(tipo, formato, inicio=None, fim=None, total_registros=0, tamanho_bytes=0, status='sucesso', mensagem=None):
    inicio = inicio or datetime.utcnow()
    fim = fim or inicio

    registro = HistoricoExportacao(
        tipo_relatorio=tipo,
        formato=formato,
        periodo_inicio=inicio,
        periodo_fim=fim,
        total_registros=total_registros,
        tamanho_bytes=tamanho_bytes,
        status=status,
        mensagem_erro=mensagem
    )
    db.session.add(registro)
    db.session.commit()
    return registro


def listar_historico(limit=20):
    limite = max(1, min(int(limit or 20), 100))
    registros = (
        HistoricoExportacao.query.order_by(HistoricoExportacao.criado_em.desc())
        .limit(limite)
        .all()
    )
    resposta = []
    for item in registros:
        resposta.append({
            'id': item.id,
            'tipo_relatorio': item.tipo_relatorio,
            'formato': item.formato,
            'periodo': f"{item.periodo_inicio.strftime('%d/%m/%Y')} - {item.periodo_fim.strftime('%d/%m/%Y')}",
            'total_registros': item.total_registros,
            'status': item.status,
            'criado_em': item.criado_em.strftime('%d/%m/%Y %H:%M'),
            'tamanho_bytes': item.tamanho_bytes
        })
    return resposta
