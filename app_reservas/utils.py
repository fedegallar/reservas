import datetime
from constance import config
from django.utils import timezone

from app_reservas.models import Aula, Laboratorio, LaboratorioInformatico, RecursoAli

def obtener_siguiente_dia_vigente(dia, horario):
    now = timezone.now()
    # Comparo el día requerido con el día actual
    # Se resta uno para mantener compatibilidades entre datos del
    # servidor académico y los datos de weekday obtenidos por python
    if now.weekday() == dia-1:
        return datetime.datetime.combine(now.date(), horario).isoformat()
    elif now.weekday() < dia-1:
        dia = now.date() + datetime.timedelta(days=(dia-1)-now.weekday())
    else:
        dia = now.date() + datetime.timedelta(days=6-(now.weekday()-dia))
    return datetime.datetime.combine(dia, horario).isoformat()


def obtener_fecha_finalizacion_reserva_cursado(cuatrimestre):
    if cuatrimestre == '1':
        fecha_fin = config.FECHA_FIN_PRIMER_SEMESTRE
        if fecha_fin.year == timezone.now().year:
            return datetime.datetime.combine(fecha_fin, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")
        else:
            return timezone.datetime(timezone.now().year, 6, 25, 23, 00).strftime("%Y%m%dT%H%M%SZ")
    if cuatrimestre == '2' or cuatrimestre == '0':
        fecha_fin = config.FECHA_FIN_SEGUNDO_SEMESTRE
        if fecha_fin.year == timezone.now().year:
            return datetime.datetime.combine(fecha_fin, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")
        else:
            return timezone.datetime(timezone.now().year, 11, 30, 23, 00).strftime("%Y%m%dT%H%M%SZ")


def obtener_fecha_finalizacion_reserva_fuera_cursado(date):
    return datetime.datetime.combine(date, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")


def obtener_fecha_inicio_reserva_cursado(cuatrimestre):
    if cuatrimestre == '1' or cuatrimestre == '0':
        fecha_inicio = config.FECHA_INICIO_PRIMER_SEMESTRE
        if fecha_inicio.year == timezone.now().year:
            return fecha_inicio
        else:
            return timezone.datetime(timezone.now().year, 3, 8,)
    if cuatrimestre == '2':
        fecha_inicio = config.FECHA_INICIO_SEGUNDO_SEMESTRE
        if fecha_inicio.year == timezone.now().year:
            return fecha_inicio
        else:
            return timezone.datetime(timezone.now().year, 8, 8,)


def obtener_fecha_fin_reserva_cursado(cuatrimestre):
    if cuatrimestre == '1':
        fecha_fin = config.FECHA_FIN_PRIMER_SEMESTRE
        if fecha_fin.year == timezone.now().year:
            return fecha_fin
        else:
            return timezone.datetime(timezone.now().year, 6, 25,)
    if cuatrimestre == '2' or cuatrimestre == '0':
        fecha_fin = config.FECHA_FIN_SEGUNDO_SEMESTRE
        if fecha_fin.year == timezone.now().year:
            return fecha_fin
        else:
            return timezone.datetime(timezone.now().year, 12, 19,)


def obtener_modelo_recurso(id):
    if Aula.objects.filter(id=id):
        return Aula
    elif LaboratorioInformatico.objects.filter(id=id):
        return LaboratorioInformatico
    elif Laboratorio.objects.filter(id=id):
        return Laboratorio
    elif RecursoAli.objects.filter(id=id):
        return RecursoAli
    else:
        return None


def obtener_recurso(id):
    model = obtener_modelo_recurso(id)
    if model:
        return model.objects.filter(id=id)[0]
    return None


def parse_time(time):
    str_time = str(time)
    if len(str_time) > 2:
        hora = "{0!s}:{1!s}".format(str_time[:-2], str_time[-2:])
    elif len(str_time) <= 2:
        hora = "{0!s}:00".format(str_time)
    return timezone.datetime.strptime(hora, "%H:%M").time()


def add_minutes_to_time(time, minutes):
    hora = (datetime.datetime.combine(datetime.date(1, 1, 1), time) + datetime.timedelta(
        minutes=minutes))
    return hora.time()


def filter_by_comision_materia_especialidad(list_json, comision, materia, especialidad):
    return [i for i in list_json if i['comision'] == comision and i['materia'] == materia and i['especialid'] == especialidad]
