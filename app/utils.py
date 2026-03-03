from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"

def parse_date(value, default=None):
    """
    Realiza o parse de uma string de data formatada como YYYY-MM-DD.
    """
    if not value:
        return default
    try:
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, DATE_FORMAT)
    except (ValueError, TypeError):
        return default

def get_date_range(inicio_str=None, fim_str=None, days_back=29):
    """
    Calcula o intervalo de datas (início e fim) com base em strings ou valores padrão.
    Retorna objetos datetime configurados para o início e fim do dia.
    """
    hoje = datetime.now()
    
    fim_date = parse_date(fim_str, hoje)
    inicio_date = parse_date(inicio_str, fim_date - timedelta(days=days_back))
    
    if inicio_date > fim_date:
        inicio_date, fim_date = fim_date, inicio_date
        
    inicio_dt = datetime.combine(inicio_date.date(), datetime.min.time())
    fim_dt = datetime.combine(fim_date.date(), datetime.max.time())
    
    return inicio_dt, fim_dt
