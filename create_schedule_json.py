#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asistente interactivo para crear archivos JSON de horarios escolares

Este script ayuda a crear archivos JSON manualmente de forma estructurada,
facilitando el proceso de transcripción desde PDFs o tablas impresas.

Author: KKG Stundenplan Team
License: MIT
"""

import json
import sys
from typing import List, Dict, Any

DIAS = {
    "1": "Lunes",
    "2": "Martes",
    "3": "Miércoles",
    "4": "Jueves",
    "5": "Viernes"
}


def mostrar_banner():
    """Muestra el banner de bienvenida."""
    print("=" * 70)
    print("  📅 Asistente de Creación de Horarios Escolares JSON")
    print("=" * 70)
    print()


def obtener_clase() -> str:
    """
    Solicita al usuario el identificador de la clase.

    Returns:
        Identificador de la clase (ej: "7d", "7e")
    """
    while True:
        clase = input("Ingresa el identificador de la clase (ej: 7d, 7e): ").strip()
        if clase:
            return clase
        print("❌ Por favor ingresa un identificador válido")


def agregar_evento() -> Dict[str, Any]:
    """
    Solicita información de un evento al usuario.

    Returns:
        Diccionario con datos del evento
    """
    print("\n" + "-" * 50)
    print("Agregar nuevo evento")
    print("-" * 50)

    # Día de la semana
    while True:
        print("\nDías disponibles:")
        for num, nombre in DIAS.items():
            print(f"  {num} = {nombre}")

        dia = input("Día (1-5): ").strip()
        if dia in DIAS:
            dia = int(dia)
            break
        print("❌ Ingresa un número entre 1 y 5")

    # Período
    while True:
        periodo = input("Período (1-12): ").strip()
        if periodo.isdigit() and 1 <= int(periodo) <= 12:
            periodo = int(periodo)
            break
        print("❌ Ingresa un número entre 1 y 12")

    # Asignatura
    asignatura = input("Asignatura (ej: m, d, f/l): ").strip()

    # Aula
    aula = input("Aula (ej: A104, A104/E02): ").strip()

    evento = {
        "dia": dia,
        "periodo": periodo,
        "asignatura": asignatura,
        "aula": aula
    }

    # Confirmación
    print("\n✓ Evento creado:")
    print(f"  {DIAS[str(dia)]} - Período {periodo}")
    print(f"  Asignatura: {asignatura}")
    print(f"  Aula: {aula}")

    return evento


def main():
    """Función principal del asistente."""
    mostrar_banner()

    # Obtener clase
    clase = obtener_clase()
    eventos: List[Dict[str, Any]] = []

    print(f"\n✓ Creando horario para clase: {clase}")
    print("\n💡 Puedes agregar eventos uno por uno.")
    print("   Presiona Ctrl+C en cualquier momento para guardar y salir.\n")

    try:
        while True:
            evento = agregar_evento()
            eventos.append(evento)

            print(f"\n📊 Total de eventos: {len(eventos)}")

            # Preguntar si desea continuar
            continuar = input("\n¿Agregar otro evento? (s/n): ").strip().lower()
            if continuar != 's':
                break

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupción detectada...")

    # Guardar JSON
    if not eventos:
        print("\n❌ No se agregaron eventos. No se guardará archivo.")
        return 1

    datos = {
        "clase": clase,
        "eventos": eventos
    }

    # Ordenar eventos por día y período
    datos["eventos"].sort(key=lambda e: (e["dia"], e["periodo"]))

    nombre_archivo = f"{clase}.json"

    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*70}")
        print(f"✓ Archivo guardado: {nombre_archivo}")
        print(f"✓ Total de eventos: {len(eventos)}")
        print(f"{'='*70}")

        print("\n📋 Próximos pasos:")
        print(f"  1. Genera el calendario: python main.py")
        print(f"  2. Copia a SubstituteFinder: cp {nombre_archivo} ../SubstituteFinder/data/")

        return 0

    except Exception as e:
        print(f"\n❌ Error al guardar: {e}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
