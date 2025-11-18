# Generador de Calendarios Escolares - Clases 7d y 7e

Este script genera archivos de calendario iCalendar (.ics) a partir de archivos JSON que contienen los horarios escolares de Diego (7d) y Mateo (7e).

## Requisitos

- Python 3.6 o superior

## Estructura del Proyecto

- `main.py`: Script principal para generar calendarios ICS
- `7d.json`: Datos para la clase 7d (Diego)
- `7e.json`: Datos para la clase 7e (Mateo)
- `output/`: Carpeta donde se guardan los calendarios ICS generados
  - `calendario_7d.ics`: Calendario para Diego (clase 7d)
  - `calendario_7e.ics`: Calendario para Mateo (clase 7e)

## Uso

Ejecutar el script principal:

```bash
python main.py
```

Por defecto, el script busca los archivos JSON en el directorio actual y guarda los archivos ICS en la carpeta "output".

Puedes especificar directorios personalizados:

```bash
python main.py --input-dir ./datos --output-dir ./calendarios
```

## Asignaturas y Profesores

### Clase 7d (Diego)
- **Alemán**: Stephan Bertelsmann
- **Latín**: Monika Weiser
- **Inglés**: Andreas Nerl / Torsten Kuchenbecker
- **Francés**: Aurélie Günther
- **Matemáticas**: Michelle Schmidt
- **Física**: Oliver Eyding
- **Informática**: Gunther Reimann
- **Historia**: Oliver Eyding
- **Geografía**: Stefan Singer
- **Arte**: Christine Görner-Fliß
- **Música**: Thomas Kraemer
- **Deportes**: Anna Güntner / Gero Hermannstaller
- **Religión Católica**: Rita Multerer
- **Religión Evangélica**: Dr. Anne Stempel
- **Ética**: Doris Teuber

### Clase 7e (Mateo)
- **Alemán**: Sarah Ziegeler
- **Latín**: Marlen Thaler
- **Inglés**: Sonja Rauscher
- **Francés**: Maren Reinicke
- **Matemáticas**: Gero Hermannstaller
- **Física**: Heidrun Frank
- **Informática**: Dimitri Tsambrounis
- **Historia**: Philipp Lehmann
- **Geografía**: Manuel Trenkle
- **Arte**: Christine Görner-Fliß
- **Música**: Jenny Kühl
- **Deportes**: Anna Güntner / Gero Hermannstaller / Florian Leszynsky
- **Religión Católica**: Amelie Döring
- **Religión Evangélica**: Dr. Anne Stempel
- **Ética**: Sonja Rauscher

## Formato JSON

El formato de los archivos JSON es el siguiente:

```json
{
  "clase": "7d",
  "eventos": [
    {
      "dia": 1,
      "periodo": 1,
      "asignatura": "d",
      "aula": "A104"
    }
  ]
}
```

- `clase`: Identificador de la clase (7d o 7e)
- `eventos`: Lista de eventos
  - `dia`: Día de la semana (1=Lunes, 2=Martes, ..., 5=Viernes)
  - `periodo`: Período del día (1-12)
  - `asignatura`: Abreviatura de la asignatura
  - `aula`: Aula donde se imparte la clase

## Abreviaturas de Asignaturas

- `m`: Matemáticas
- `d`: Alemán
- `e`: Inglés
- `g`: Historia
- `f`: Francés
- `l`: Latín
- `geo`: Geografía
- `ku`: Arte
- `mu`: Música
- `sw/sm`: Deportes
- `ntph`: Física
- `ntinf7`: Informática
- `ev`: Religión Evangélica
- `k`: Religión Católica
- `eth`: Ética
- `intm`: Intensivo Matemáticas
- `intl`: Intensivo Latín
- `intf`: Intensivo Francés
- `DaZ-plus7`: Alemán Plus 7
- `ffme`: Actividad después de clases

## Comprobación de los ICS generados

Puedes validar los archivos .ics generados en:
https://icalendar.org/validator.html

## Importación en Google Calendar

1. Descarga los archivos .ics generados desde la carpeta `output/`
2. En Google Calendar, ve a **Configuración > Importar y exportar**
3. Selecciona el archivo .ics descargado
4. Selecciona el calendario donde deseas importar los eventos
5. Haz clic en "Importar"

**Nota**: Importa `calendario_7d.ics` en el calendario de Diego y `calendario_7e.ics` en el calendario de Mateo.

## Notas

- Los archivos generados utilizan la zona horaria de Berlín (Europe/Berlin)
- Los eventos se programan para ser recurrentes semanalmente hasta el 1 de agosto de 2025
- El inicio del calendario se establece a partir del 31 de marzo de 2025 (primer lunes)
- Las clases divididas (e.g., "f/l" o "e/e") indican grupos divididos en diferentes aulas

## Solución de problemas

Si tienes problemas al importar los archivos .ics:

1. Verifica que los archivos JSON estén correctamente formateados
2. Asegúrate de que los finales de línea sean CRLF (Windows)
3. Valida los archivos .ics en https://icalendar.org/validator.html antes de importar
4. Si Google Calendar no acepta el archivo, intenta importarlo en otro cliente de calendario (Apple Calendar, Outlook) para identificar el problema