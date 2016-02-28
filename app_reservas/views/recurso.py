# coding=utf-8

import json
from dateutil.parser import parse

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app_reservas.models import Recurso


def recurso_eventos_json(request, pk):
    # Indica la ruta donde se almacenan los archivos JSON de eventos de recursos.
    ruta_archivos = 'media/app_reservas/eventos_recursos/'

    # Obtiene el recurso especificado.
    recurso = get_object_or_404(Recurso, pk=pk)

    # Arma el nombre del archivo.
    nombre_archivo = str(recurso.id) + '.json'
    nombre_archivo_completo = ruta_archivos + nombre_archivo

    # Inicializa la lista de eventos a retornar.
    eventos = []

    # Lee el archivo de eventos del recurso actual.
    with open(nombre_archivo_completo, 'r') as archivo:
        # Parsea el contenido del archivo JSON.
        data = json.load(archivo)

    # Verifica que los parámetros de intervalo de fechas hayan sido
    # especificados.
    if 'start' in request.GET and 'end' in request.GET:
        # Parsea las fechas de inicio y fin indicadas.
        fecha_inicio = parse(request.GET['start']).date()
        fecha_fin = parse(request.GET['end']).date()

        # Recorre todos los eventos, en busca de aquellos que se correspondan
        # con el intervalo requerido.
        for evento in data:
            evento_inicio = parse(evento['start']).date()
            if fecha_inicio <= evento_inicio <= fecha_fin:
                # Añade el evento a la lista a retornar.
                eventos.append(evento)
    else:
        # Si no se especifica intervalo, retorna todos los eventos del aula.
        eventos = data

    # Serializa la respuesta en formato JSON. Se requiere el parámetro 'safe'
    # en falso, debido a que se retorna una lista y no un diccionario.
    return JsonResponse(eventos, safe=False)
