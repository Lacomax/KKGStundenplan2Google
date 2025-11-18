#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import argparse
from datetime import datetime
from datetime import timedelta

# Definiciones globales
DIAS_SEMANA = ["", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
DIAS_RRULE = ["", "MO", "TU", "WE", "TH", "FR"]
HORARIOS = [
    {"inicio": "08:10", "fin": "08:55"},
    {"inicio": "08:55", "fin": "09:40"},
    {"inicio": "10:00", "fin": "10:45"},
    {"inicio": "10:45", "fin": "11:30"},
    {"inicio": "11:45", "fin": "12:30"},
    {"inicio": "12:30", "fin": "13:15"},
    {"inicio": "13:30", "fin": "14:15"},
    {"inicio": "14:15", "fin": "15:00"},
    {"inicio": "15:00", "fin": "15:45"},
    {"inicio": "15:45", "fin": "16:30"},
    {"inicio": "16:30", "fin": "17:15"},
    {"inicio": "17:15", "fin": "18:00"}
]

# Mapeo de abreviaturas a nombres completos
ASIGNATURAS = {
    "m": "Matemáticas",
    "d": "Alemán",
    "e": "Inglés",
    "g": "Historia",
    "f": "Francés",
    "l": "Latín",
    "ku": "Arte",
    "mu": "Música",
    "sw": "Deportes",
    "sm": "Deportes",
    "geo": "Geografía",
    "ntbio": "Biología",
    "ntinf": "Informática",
    "ntinf7": "Informática",
    "ntph": "Física",
    "ev": "Religión Evangélica",
    "k": "Religión Católica",
    "eth": "Ética",
    "qhu": "Hora de estudio",
    "qhu6": "Hora de estudio 6",
    "mint": "MINT",
    "fint": "Intensivo Francés",
    "intf": "Intensivo Francés",
    "lint": "Intensivo Latín",
    "intl": "Intensivo Latín",
    "intm": "Intensivo Matemáticas",
    "DaZ-plus7": "Alemán Plus 7",
    "ffmm-gta": "Actividad después de clases",
    "ffmd-gta": "Actividad después de clases",
    "ffme-gta": "Actividad después de clases",
    "ffme": "Actividad después de clases",
    "mittag": "Almuerzo"
}

def cargar_json(nombre_archivo):
    """Carga los datos desde un archivo JSON."""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al leer {nombre_archivo}: {e}")
        return None

def formatear_fecha(fecha, hora):
    """Formatea una fecha y hora para iCalendar sin zona horaria."""
    horas, minutos = map(int, hora.split(':'))
    year = fecha.year
    month = fecha.month
    day = fecha.day
    
    return f"{year}{month:02d}{day:02d}T{horas:02d}{minutos:02d}00"

def obtener_timestamp():
    """Obtiene el timestamp actual en formato iCalendar."""
    ahora = datetime.now()
    return f"{ahora.year}{ahora.month:02d}{ahora.day:02d}T{ahora.hour:02d}{ahora.minute:02d}{ahora.second:02d}Z"

def generar_icalendar(datos_clase):
    """Genera un archivo iCalendar para una clase."""
    if not datos_clase:
        return None
        
    clase = datos_clase["clase"]
    eventos = datos_clase["eventos"]
    
    # Fecha base para los eventos (próximo lunes desde hoy)
    hoy = datetime.now()
    dias_hasta_lunes = (7 - hoy.weekday()) % 7
    if dias_hasta_lunes == 0:
        dias_hasta_lunes = 7
    fecha_base = hoy + timedelta(days=dias_hasta_lunes)
    
    # Fecha de fin de curso (6 meses desde hoy)
    fecha_fin = hoy + timedelta(days=180)
    fecha_fin_curso = f"{fecha_fin.year}{fecha_fin.month:02d}{fecha_fin.day:02d}T235959Z"
    
    # Timestamp para DTSTAMP
    dtstamp = obtener_timestamp()
    
    # Encabezado iCalendar con definición de zona horaria
    lines = []
    lines.append("BEGIN:VCALENDAR")
    lines.append("VERSION:2.0")
    lines.append(f"PRODID:-//HorarioEscolar//Clase {clase}//ES")
    lines.append("CALSCALE:GREGORIAN")
    lines.append("METHOD:PUBLISH")
    lines.append(f"X-WR-CALNAME:Clase {clase}")
    
    # Definición de zona horaria
    lines.append("BEGIN:VTIMEZONE")
    lines.append("TZID:Europe/Berlin")
    lines.append("X-LIC-LOCATION:Europe/Berlin")
    lines.append("BEGIN:DAYLIGHT")
    lines.append("TZOFFSETFROM:+0100")
    lines.append("TZOFFSETTO:+0200")
    lines.append("TZNAME:CEST")
    lines.append("DTSTART:19700329T020000")
    lines.append("RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU")
    lines.append("END:DAYLIGHT")
    lines.append("BEGIN:STANDARD")
    lines.append("TZOFFSETFROM:+0200")
    lines.append("TZOFFSETTO:+0100")
    lines.append("TZNAME:CET")
    lines.append("DTSTART:19701025T030000")
    lines.append("RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU")
    lines.append("END:STANDARD")
    lines.append("END:VTIMEZONE")
    
    # Generar eventos
    for i, evento in enumerate(eventos):
        # Obtener detalles del evento
        dia_semana = evento["dia"]
        periodo = evento["periodo"]
        asignatura_abrev = evento["asignatura"]
        aula = evento["aula"]
        
        # Crear fecha para este evento
        fecha_evento = fecha_base + timedelta(days=(dia_semana - 1))
        
        # Obtener horario
        if periodo <= len(HORARIOS):
            hora_inicio = HORARIOS[periodo - 1]["inicio"]
            hora_fin = HORARIOS[periodo - 1]["fin"]
        else:
            continue  # Saltar si el período está fuera de rango
        
        # Formatear fechas
        dtstart = formatear_fecha(fecha_evento, hora_inicio)
        dtend = formatear_fecha(fecha_evento, hora_fin)
        
        # Generar el nombre completo de la asignatura
        partes_asignatura = asignatura_abrev.split('/')
        nombres_asignatura = []
        
        for parte in partes_asignatura:
            if parte in ASIGNATURAS:
                nombres_asignatura.append(ASIGNATURAS[parte])
            else:
                nombres_asignatura.append(parte)
        
        nombre_asignatura = '/'.join(nombres_asignatura)
        
        # Generar UID único
        uid = f"clase{clase}-{i}@example.com"
        
        # Añadir evento con RRULE para repetición semanal
        lines.append("BEGIN:VEVENT")
        lines.append(f"DTSTART;TZID=Europe/Berlin:{dtstart}")
        lines.append(f"DTEND;TZID=Europe/Berlin:{dtend}")
        lines.append(f"DTSTAMP:{dtstamp}")
        lines.append(f"UID:{uid}")
        lines.append(f"RRULE:FREQ=WEEKLY;WKST=MO;BYDAY={DIAS_RRULE[dia_semana]};UNTIL={fecha_fin_curso}")
        lines.append(f"SUMMARY:{nombre_asignatura}")
        lines.append(f"LOCATION:{aula}")
        lines.append(f"DESCRIPTION:{DIAS_SEMANA[dia_semana]} - Clase {clase}")
        lines.append("END:VEVENT")
    
    # Cerrar calendario
    lines.append("END:VCALENDAR")
    
    # Unir todas las líneas con CRLF como separador
    ical = "\r\n".join(lines) + "\r\n"
    
    return ical

def guardar_icalendar(ical, nombre_archivo):
    """Guarda el contenido iCalendar en un archivo."""
    if not ical:
        return False
        
    try:
        # Importante: abrir en modo binario para preservar CRLF
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(ical.encode('utf-8'))
        print(f"Archivo {nombre_archivo} generado con éxito.")
        return True
    except Exception as e:
        print(f"Error al guardar {nombre_archivo}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generador de calendarios escolares')
    parser.add_argument('--input-dir', default='.', help='Directorio de entrada para archivos JSON')
    parser.add_argument('--output-dir', default='output', help='Directorio de salida para archivos ICS')
    args = parser.parse_args()
    
    # Crear directorio de salida si no existe
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Cargar datos desde archivos JSON
    json_7d_path = os.path.join(args.input_dir, '7d.json')
    json_7e_path = os.path.join(args.input_dir, '7e.json')
    
    datos_7d = cargar_json(json_7d_path)
    datos_7e = cargar_json(json_7e_path)
    
    if not datos_7d:
        print(f"No se pudo cargar {json_7d_path}. Asegúrate de que el archivo existe.")
    if not datos_7e:
        print(f"No se pudo cargar {json_7e_path}. Asegúrate de que el archivo existe.")
    
    # Generar calendarios desde los JSON
    ical_7d = generar_icalendar(datos_7d)
    ical_7e = generar_icalendar(datos_7e)
    
    # Guardar calendarios
    salida_7d = os.path.join(args.output_dir, 'calendario_7d.ics')
    salida_7e = os.path.join(args.output_dir, 'calendario_7e.ics')
    
    exito_7d = guardar_icalendar(ical_7d, salida_7d)
    exito_7e = guardar_icalendar(ical_7e, salida_7e)
    
    if exito_7d or exito_7e:
        print(f"Proceso completado. Revisa la carpeta '{args.output_dir}' para los archivos generados.")
    else:
        print("No se pudo generar ningún calendario.")

if __name__ == "__main__":
    main()