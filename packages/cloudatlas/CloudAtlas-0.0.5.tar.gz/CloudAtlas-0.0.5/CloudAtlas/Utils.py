from datetime import datetime, timedelta
from pytz import timezone


def extract_time(day):
    dia = day.strftime("%d")
    mes = day.strftime("%m")
    ano = day.strftime("%Y")
    return dict(dia=dia, mes=mes, ano=ano)


def today(tz='America/Sao_Paulo'):
    hoje = timezone(tz).localize(datetime.today())
    return hoje, extract_time(hoje)


def yesterday(tz='America/Sao_Paulo', days=1):
    hoje, _ = today()
    ontem = hoje + timedelta(days=-days)
    return ontem, extract_time(ontem)
