#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Calendarios Escolares

Este módulo convierte horarios escolares desde archivos JSON a formato iCalendar (.ics)
para facilitar la importación en Google Calendar y otros clientes de calendario.

Author: KKG Stundenplan Team
License: MIT
"""

import json
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# ============================================================================
# CONSTANTES GLOBALES
# ============================================================================

# Configuración de calendario
DIAS_SEMANA = ["", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
DIAS_RRULE = ["", "MO", "TU", "WE", "TH", "FR"]
DIAS_CURSO_ESCOLAR = 180  # Duración del curso escolar en días
TIMEZONE = "Europe/Berlin"
PRODID_PREFIX = "-//HorarioEscolar//Clase"

# Horarios de clase (formato 24h)
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

def cargar_json(nombre_archivo: str) -> Optional[Dict[str, Any]]:
    """
    Carga los datos desde un archivo JSON.

    Args:
        nombre_archivo: Ruta al archivo JSON a cargar

    Returns:
        Diccionario con los datos del JSON o None si hay error

    Raises:
        No lanza excepciones, las captura y retorna None

    Example:
        >>> datos = cargar_json('7d.json')
        >>> if datos:
        ...     print(datos['clase'])
        7d
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            # Validación básica de estructura
            if not isinstance(datos, dict):
                logging.error(f"{nombre_archivo}: El archivo debe contener un objeto JSON")
                return None
            if 'clase' not in datos or 'eventos' not in datos:
                logging.error(f"{nombre_archivo}: Faltan campos requeridos 'clase' o 'eventos'")
                return None
            return datos
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {nombre_archivo}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error al decodificar JSON en {nombre_archivo}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error inesperado al leer {nombre_archivo}: {e}")
        return None

def formatear_fecha(fecha: datetime, hora: str) -> str:
    """
    Formatea una fecha y hora para el formato iCalendar.

    Args:
        fecha: Objeto datetime con la fecha
        hora: Hora en formato "HH:MM"

    Returns:
        Cadena en formato iCalendar "YYYYMMDDTHHmmss"

    Example:
        >>> from datetime import datetime
        >>> fecha = datetime(2025, 3, 31)
        >>> formatear_fecha(fecha, "08:10")
        '20250331T081000'
    """
    horas, minutos = map(int, hora.split(':'))
    return f"{fecha.year}{fecha.month:02d}{fecha.day:02d}T{horas:02d}{minutos:02d}00"

def obtener_timestamp() -> str:
    """
    Obtiene el timestamp actual en formato iCalendar UTC.

    Returns:
        Timestamp en formato "YYYYMMDDTHHmmssZ"

    Example:
        >>> timestamp = obtener_timestamp()
        >>> len(timestamp)
        16
        >>> timestamp.endswith('Z')
        True
    """
    ahora = datetime.now()
    return f"{ahora.year}{ahora.month:02d}{ahora.day:02d}T{ahora.hour:02d}{ahora.minute:02d}{ahora.second:02d}Z"

def validar_evento(evento: Dict[str, Any], indice: int) -> bool:
    """
    Valida que un evento tenga todos los campos requeridos.

    Args:
        evento: Diccionario con datos del evento
        indice: Índice del evento para mensajes de error

    Returns:
        True si el evento es válido, False en caso contrario
    """
    campos_requeridos = ['dia', 'periodo', 'asignatura', 'aula']
    for campo in campos_requeridos:
        if campo not in evento:
            logging.warning(f"Evento {indice}: falta el campo '{campo}'")
            return False

    # Validar rangos
    if not (1 <= evento['dia'] <= 5):
        logging.warning(f"Evento {indice}: día {evento['dia']} fuera de rango (1-5)")
        return False

    if not (1 <= evento['periodo'] <= len(HORARIOS)):
        logging.warning(f"Evento {indice}: período {evento['periodo']} fuera de rango (1-{len(HORARIOS)})")
        return False

    return True


def generar_icalendar(datos_clase: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Genera un archivo iCalendar para una clase.

    Args:
        datos_clase: Diccionario con la estructura:
            {
                "clase": "7d",
                "eventos": [
                    {"dia": 1, "periodo": 1, "asignatura": "m", "aula": "A104"},
                    ...
                ]
            }

    Returns:
        Contenido del archivo iCalendar en formato string o None si hay error

    Example:
        >>> datos = {"clase": "7d", "eventos": [{"dia": 1, "periodo": 1, "asignatura": "m", "aula": "A104"}]}
        >>> ical = generar_icalendar(datos)
        >>> ical is not None
        True
        >>> 'BEGIN:VCALENDAR' in ical
        True
    """
    if not datos_clase:
        logging.error("No se proporcionaron datos de clase")
        return None

    clase = datos_clase.get("clase", "Unknown")
    eventos = datos_clase.get("eventos", [])

    if not eventos:
        logging.warning(f"Clase {clase}: no tiene eventos para procesar")
        return None

    # Fecha base para los eventos (próximo lunes desde hoy)
    hoy = datetime.now()
    dias_hasta_lunes = (7 - hoy.weekday()) % 7
    if dias_hasta_lunes == 0:
        dias_hasta_lunes = 7
    fecha_base = hoy + timedelta(days=dias_hasta_lunes)

    # Fecha de fin de curso
    fecha_fin = hoy + timedelta(days=DIAS_CURSO_ESCOLAR)
    fecha_fin_curso = f"{fecha_fin.year}{fecha_fin.month:02d}{fecha_fin.day:02d}T235959Z"
    
    # Timestamp para DTSTAMP
    dtstamp = obtener_timestamp()
    
    # Encabezado iCalendar con definición de zona horaria
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{PRODID_PREFIX} {clase}//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:Clase {clase}"
    ]
    
    # Definición de zona horaria
    lines.extend([
        "BEGIN:VTIMEZONE",
        f"TZID:{TIMEZONE}",
        f"X-LIC-LOCATION:{TIMEZONE}"
    ])
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
    eventos_procesados = 0
    for i, evento in enumerate(eventos):
        # Validar evento
        if not validar_evento(evento, i):
            continue

        # Obtener detalles del evento
        dia_semana = evento["dia"]
        periodo = evento["periodo"]
        asignatura_abrev = evento["asignatura"]
        aula = evento["aula"]

        # Crear fecha para este evento
        fecha_evento = fecha_base + timedelta(days=(dia_semana - 1))

        # Obtener horario (el período ya fue validado)
        hora_inicio = HORARIOS[periodo - 1]["inicio"]
        hora_fin = HORARIOS[periodo - 1]["fin"]
        
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

        # Generar UID único basado en clase, día, período y hash temporal
        # Esto evita conflictos cuando se reimporta el calendario
        uid = f"clase{clase}-d{dia_semana}p{periodo}-{dtstamp}@kkg-stundenplan.local"
        
        # Añadir evento con RRULE para repetición semanal
        lines.extend([
            "BEGIN:VEVENT",
            f"DTSTART;TZID={TIMEZONE}:{dtstart}",
            f"DTEND;TZID={TIMEZONE}:{dtend}",
            f"DTSTAMP:{dtstamp}",
            f"UID:{uid}",
            f"RRULE:FREQ=WEEKLY;WKST=MO;BYDAY={DIAS_RRULE[dia_semana]};UNTIL={fecha_fin_curso}",
            f"SUMMARY:{nombre_asignatura}",
            f"LOCATION:{aula}",
            f"DESCRIPTION:{DIAS_SEMANA[dia_semana]} - Clase {clase}",
            "END:VEVENT"
        ])
        eventos_procesados += 1
    
    # Cerrar calendario
    lines.append("END:VCALENDAR")

    # Verificar que se procesó al menos un evento
    if eventos_procesados == 0:
        logging.warning(f"Clase {clase}: ningún evento válido para procesar")
        return None

    logging.info(f"Clase {clase}: {eventos_procesados} de {len(eventos)} eventos procesados correctamente")

    # Unir todas las líneas con CRLF como separador (estándar iCalendar)
    ical = "\r\n".join(lines) + "\r\n"

    return ical

def guardar_icalendar(ical: Optional[str], nombre_archivo: str) -> bool:
    """
    Guarda el contenido iCalendar en un archivo.

    Args:
        ical: Contenido del calendario en formato iCalendar
        nombre_archivo: Ruta donde guardar el archivo

    Returns:
        True si se guardó exitosamente, False en caso contrario

    Note:
        El archivo se abre en modo binario para preservar los finales
        de línea CRLF requeridos por el estándar iCalendar.
    """
    if not ical:
        logging.warning("No hay contenido iCalendar para guardar")
        return False

    try:
        # Importante: abrir en modo binario para preservar CRLF
        archivo_path = Path(nombre_archivo)
        archivo_path.parent.mkdir(parents=True, exist_ok=True)

        with open(archivo_path, 'wb') as archivo:
            archivo.write(ical.encode('utf-8'))

        logging.info(f"Archivo {nombre_archivo} generado con éxito")
        print(f"✓ Archivo {nombre_archivo} generado con éxito")
        return True
    except PermissionError:
        logging.error(f"Sin permisos para escribir en {nombre_archivo}")
        return False
    except Exception as e:
        logging.error(f"Error al guardar {nombre_archivo}: {e}")
        return False

def main() -> int:
    """
    Función principal del programa.

    Returns:
        Código de salida: 0 si éxito, 1 si error
    """
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description='Generador de calendarios escolares iCalendar (.ics) desde archivos JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s
  %(prog)s --input-dir ./datos --output-dir ./calendarios
  %(prog)s --verbose
        """
    )
    parser.add_argument(
        '--input-dir',
        default='.',
        help='Directorio de entrada para archivos JSON (default: directorio actual)'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Directorio de salida para archivos ICS (default: output)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar información detallada de depuración'
    )
    args = parser.parse_args()

    # Configurar logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )

    # Usar pathlib para manejo de rutas
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    # Crear directorio de salida si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.debug(f"Directorio de salida: {output_dir.absolute()}")

    # Cargar datos desde archivos JSON
    json_7d_path = input_dir / '7d.json'
    json_7e_path = input_dir / '7e.json'

    datos_7d = cargar_json(str(json_7d_path))
    datos_7e = cargar_json(str(json_7e_path))

    # Generar calendarios desde los JSON
    ical_7d = generar_icalendar(datos_7d)
    ical_7e = generar_icalendar(datos_7e)

    # Guardar calendarios
    salida_7d = output_dir / 'calendario_7d.ics'
    salida_7e = output_dir / 'calendario_7e.ics'

    exito_7d = guardar_icalendar(ical_7d, str(salida_7d))
    exito_7e = guardar_icalendar(ical_7e, str(salida_7e))

    # Resumen final
    if exito_7d or exito_7e:
        print(f"\n✓ Proceso completado. Revisa la carpeta '{output_dir}' para los archivos generados.")
        if exito_7d and exito_7e:
            return 0
        else:
            logging.warning("Solo se generó parcialmente algunos calendarios")
            return 1
    else:
        print("\n✗ No se pudo generar ningún calendario.")
        logging.error("Verifica los archivos JSON y vuelve a intentar")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())