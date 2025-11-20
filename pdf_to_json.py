#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de Horarios desde PDF a JSON

Este módulo extrae automáticamente horarios escolares desde archivos PDF
y los convierte al formato JSON utilizado por este proyecto y SubstituteFinder.

Author: KKG Stundenplan Team
License: MIT
"""

import re
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# ============================================================================
# CONSTANTES
# ============================================================================

DIAS_SEMANA = {
    "Montag": 1,
    "Dienstag": 2,
    "Mittwoch": 3,
    "Donnerstag": 4,
    "Freitag": 5
}

HORARIOS_PERIODO = {
    "08.10 - 08.55": 1,
    "08.55 - 09.40": 2,
    "10.00 - 10.45": 3,
    "10.45 - 11.30": 4,
    "11.45 - 12.30": 5,
    "12.30 - 13.15": 6,
    "13.30 - 14.15": 7,
    "14.15 - 15.00": 8,
    "15.00 - 15.45": 9,
    "15.45 - 16.30": 10,
    "16.30 - 17.15": 11,
    "17.15 - 18.00": 12
}


def extraer_texto_pdf(ruta_pdf: str) -> Optional[str]:
    """
    Extrae el texto completo de un archivo PDF.

    Args:
        ruta_pdf: Ruta al archivo PDF

    Returns:
        Texto extraído del PDF o None si hay error

    Note:
        Requiere PyPDF2. Si no está instalado, muestra instrucciones.
    """
    if PyPDF2 is None:
        logging.error("PyPDF2 no está instalado.")
        print("\n❌ PyPDF2 no encontrado. Por favor instálalo:")
        print("   pip install PyPDF2")
        return None

    try:
        with open(ruta_pdf, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            texto = ""
            for pagina in lector.pages:
                texto += pagina.extract_text()
            return texto
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {ruta_pdf}")
        return None
    except Exception as e:
        logging.error(f"Error al leer PDF {ruta_pdf}: {e}")
        return None


def extraer_clase_del_titulo(texto: str) -> Optional[str]:
    """
    Extrae el identificador de clase del título del PDF.

    Args:
        texto: Texto del PDF

    Returns:
        Identificador de clase (ej: "7d", "7e") o None

    Example:
        >>> texto = "Stundenplan der Klasse 7d\\n..."
        >>> extraer_clase_del_titulo(texto)
        '7d'
    """
    # Buscar patrón "Stundenplan der Klasse XX"
    patron = r"Stundenplan der Klasse (\w+)"
    match = re.search(patron, texto)

    if match:
        clase = match.group(1)
        logging.info(f"Clase detectada: {clase}")
        return clase

    logging.warning("No se pudo detectar la clase en el título")
    return None


def parsear_celda_horario(texto_celda: str) -> Optional[Tuple[str, str]]:
    """
    Parsea una celda de horario extrayendo asignatura y aula.

    Args:
        texto_celda: Texto de la celda (ej: "d\\nA104" o "f/l\\nA104/E02")

    Returns:
        Tupla (asignatura, aula) o None si la celda está vacía

    Example:
        >>> parsear_celda_horario("d\\nA104")
        ('d', 'A104')
        >>> parsear_celda_horario("f/l\\nA104/E02")
        ('f/l', 'A104/E02')
    """
    if not texto_celda or texto_celda.strip() == "":
        return None

    # Dividir por saltos de línea
    lineas = [l.strip() for l in texto_celda.strip().split('\n') if l.strip()]

    if len(lineas) < 2:
        return None

    asignatura = lineas[0]
    aula = lineas[1]

    return (asignatura, aula)


def extraer_eventos_desde_texto(texto: str) -> Optional[List[Dict[str, Any]]]:
    """
    Extrae eventos del horario desde el texto del PDF.

    Args:
        texto: Texto completo del PDF

    Returns:
        Lista de eventos en formato diccionario

    Note:
        Este es un parser simplificado. Para PDFs más complejos,
        considera usar pdfplumber o tabula-py para mejor extracción.
    """
    eventos = []

    # Esta es una implementación simplificada basada en patrones de texto
    # Para producción, recomiendo usar pdfplumber que puede extraer tablas

    logging.warning("Usando parser de texto simple. Para mejor precisión, usa pdfplumber.")
    logging.info("Ejecuta: pip install pdfplumber")

    # Buscar patrones de día + asignatura + aula
    # Formato esperado: después de cada día viene una lista de asignaturas
    lineas = texto.split('\n')

    dia_actual = None
    periodo_actual = None

    for i, linea in enumerate(lineas):
        linea = linea.strip()

        # Detectar día de la semana
        if linea in DIAS_SEMANA:
            dia_actual = DIAS_SEMANA[linea]
            continue

        # Detectar período por horario
        if linea in HORARIOS_PERIODO:
            periodo_actual = HORARIOS_PERIODO[linea]
            continue

        # Si tenemos día y período, buscar asignatura/aula
        if dia_actual and periodo_actual and linea:
            # Verificar si la siguiente línea podría ser el aula
            if i + 1 < len(lineas):
                siguiente = lineas[i + 1].strip()
                # Si parece un código de aula (empieza con letra y tiene números)
                if re.match(r'^[A-Z]', siguiente):
                    eventos.append({
                        "dia": dia_actual,
                        "periodo": periodo_actual,
                        "asignatura": linea,
                        "aula": siguiente
                    })
                    # Reset para próximo evento
                    dia_actual = None
                    periodo_actual = None

    return eventos if eventos else None


def convertir_pdf_a_json(ruta_pdf: str, ruta_salida: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Convierte un PDF de horario escolar a formato JSON.

    Args:
        ruta_pdf: Ruta al archivo PDF de entrada
        ruta_salida: Ruta opcional donde guardar el JSON

    Returns:
        Diccionario con datos del horario o None si hay error

    Example:
        >>> datos = convertir_pdf_a_json("Stundenplan der Klasse 7d.pdf")
        >>> datos['clase']
        '7d'
    """
    logging.info(f"Procesando PDF: {ruta_pdf}")

    # Extraer texto del PDF
    texto = extraer_texto_pdf(ruta_pdf)
    if not texto:
        return None

    # Extraer clase
    clase = extraer_clase_del_titulo(texto)
    if not clase:
        # Intentar extraer del nombre del archivo
        nombre_archivo = Path(ruta_pdf).stem
        match = re.search(r'(\d+[a-z])', nombre_archivo.lower())
        if match:
            clase = match.group(1)
            logging.info(f"Clase extraída del nombre de archivo: {clase}")
        else:
            logging.error("No se pudo determinar la clase")
            return None

    # Extraer eventos
    eventos = extraer_eventos_desde_texto(texto)
    if not eventos:
        logging.error("No se pudieron extraer eventos del PDF")
        logging.info("💡 Sugerencia: Este PDF puede requerir extracción manual o pdfplumber")
        return None

    # Crear estructura JSON
    datos = {
        "clase": clase,
        "eventos": eventos
    }

    # Guardar si se especificó ruta de salida
    if ruta_salida:
        try:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            logging.info(f"✓ JSON guardado en: {ruta_salida}")
            print(f"✓ JSON generado: {ruta_salida}")
        except Exception as e:
            logging.error(f"Error al guardar JSON: {e}")
            return None

    return datos


def main() -> int:
    """
    Función principal del extractor PDF → JSON.

    Returns:
        Código de salida: 0 si éxito, 1 si error
    """
    parser = argparse.ArgumentParser(
        description='Extrae horarios escolares desde PDF y genera archivos JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s "Stundenplan der Klasse 7d.pdf"
  %(prog)s "Stundenplan der Klasse 7d.pdf" --output 7d.json
  %(prog)s horarios/*.pdf --output-dir ./data
  %(prog)s --help

Nota: Este extractor usa PyPDF2 para lectura básica de texto.
Para mejores resultados con PDFs complejos, considera instalar pdfplumber:
  pip install pdfplumber

Integración con SubstituteFinder:
  Los archivos JSON generados son compatibles con el repositorio
  SubstituteFinder para monitoreo de sustituciones de profesores.
        """
    )

    parser.add_argument(
        'pdf_files',
        nargs='+',
        help='Archivo(s) PDF de horario escolar'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo JSON de salida (solo para un PDF)'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Directorio de salida para múltiples PDFs'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar información detallada'
    )

    args = parser.parse_args()

    # Configurar logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )

    # Verificar PyPDF2
    if PyPDF2 is None:
        print("\n❌ Dependencia faltante: PyPDF2")
        print("   Instálala con: pip install PyPDF2")
        print("\n💡 Para mejores resultados: pip install pdfplumber")
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exitos = 0
    for pdf_file in args.pdf_files:
        # Determinar ruta de salida
        if args.output and len(args.pdf_files) == 1:
            ruta_salida = args.output
        else:
            # Generar nombre automático basado en el PDF
            nombre_base = Path(pdf_file).stem
            # Intentar extraer clase del nombre
            match = re.search(r'(\d+[a-z])', nombre_base.lower())
            if match:
                clase = match.group(1)
                ruta_salida = output_dir / f"{clase}.json"
            else:
                ruta_salida = output_dir / f"{nombre_base}.json"

        # Convertir
        resultado = convertir_pdf_a_json(pdf_file, str(ruta_salida))
        if resultado:
            exitos += 1

    # Resumen
    print(f"\n{'='*60}")
    if exitos > 0:
        print(f"✓ {exitos} de {len(args.pdf_files)} archivo(s) procesado(s) exitosamente")
        print(f"\n💡 Los archivos JSON están listos para:")
        print(f"   • Generar calendarios .ics con: python main.py")
        print(f"   • Monitorear sustituciones con SubstituteFinder")
        return 0
    else:
        print(f"✗ No se pudo procesar ningún archivo")
        print(f"\n💡 Este extractor usa un parser simple de texto.")
        print(f"   Para PDFs complejos, considera:")
        print(f"   1. Instalar pdfplumber: pip install pdfplumber")
        print(f"   2. Extracción manual del PDF a JSON")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
