# 📅 Generador de Calendarios Escolares KKG

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-optimized-brightgreen.svg)](https://github.com/Lacomax/KKGStundenplan2Google)

Este script genera archivos de calendario iCalendar (.ics) a partir de archivos JSON que contienen los horarios escolares de las clases 7d y 7e, facilitando la importación a Google Calendar y otros clientes de calendario.

## 🚀 Características

- ✅ Conversión automática de JSON a formato iCalendar (.ics)
- ✅ Soporte para zona horaria Europe/Berlin
- ✅ Eventos recurrentes semanales con validación de datos
- ✅ Type hints completos para mejor mantenibilidad
- ✅ Logging detallado con modo verbose
- ✅ Validación robusta de datos de entrada
- ✅ Gestión automática de directorios

## 📋 Requisitos

- Python 3.6 o superior
- No requiere dependencias externas para la funcionalidad principal (solo biblioteca estándar)
- **Opcional**: PyPDF2 para extracción automática de PDFs (ver [Extracción de PDFs](#-extracción-automática-desde-pdf))

## 📁 Estructura del Proyecto

```
KKGStundenplan2Google/
├── main.py                          # ⭐ Script principal: JSON → ICS
├── create_schedule_json.py          # 🛠️  Asistente interactivo para crear JSON
├── pdf_to_json.py                   # 📄 Extractor experimental: PDF → JSON
├── 7d.json                          # 📋 Datos horario clase 7d
├── 7e.json                          # 📋 Datos horario clase 7e
├── Stundenplan der Klasse 7d.pdf    # 📑 PDF original clase 7d
├── Stundenplan der Klasse 7e.pdf    # 📑 PDF original clase 7e
├── requirements.txt                 # 📦 Dependencias opcionales
├── LICENSE                          # ⚖️  Licencia MIT
├── .gitignore                       # 🙈 Archivos ignorados por Git
└── output/                          # 📅 Calendarios generados
    ├── calendario_7d.ics
    └── calendario_7e.ics
```

## 🔧 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/Lacomax/KKGStundenplan2Google.git
cd KKGStundenplan2Google
```

2. No se requieren dependencias adicionales, solo Python 3.6+

## 💻 Uso

### Uso básico

Ejecutar el script principal:

```bash
python main.py
```

Por defecto, el script busca los archivos JSON en el directorio actual y guarda los archivos ICS en la carpeta `output/`.

### Opciones avanzadas

Especificar directorios personalizados:

```bash
python main.py --input-dir ./datos --output-dir ./calendarios
```

Activar modo verbose para depuración:

```bash
python main.py --verbose
```

Ver todas las opciones disponibles:

```bash
python main.py --help
```

## 📄 Creación de Archivos JSON

Existen tres formas de crear los archivos JSON de horarios:

### Opción 1: Asistente Interactivo (Recomendado)

La forma más fácil es usar el asistente interactivo:

```bash
python create_schedule_json.py
```

El asistente te guiará paso a paso:
1. Ingresa el identificador de la clase (ej: 7d)
2. Agrega eventos uno por uno indicando:
   - Día de la semana (1-5)
   - Período (1-12)
   - Asignatura
   - Aula
3. El script guardará automáticamente el archivo JSON

### Opción 2: Creación Manual

Crea un archivo JSON con esta estructura:

```json
{
  "clase": "7d",
  "eventos": [
    {
      "dia": 1,
      "periodo": 1,
      "asignatura": "d",
      "aula": "A104"
    },
    {
      "dia": 1,
      "periodo": 2,
      "asignatura": "d",
      "aula": "A104"
    }
  ]
}
```

**Campos requeridos:**
- `dia`: 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes
- `periodo`: 1-12 (número del período)
- `asignatura`: Código de asignatura (ej: "m", "d", "f/l")
- `aula`: Código del aula (ej: "A104", "A104/E02")

### Opción 3: Extracción desde PDF (Experimental)

**⚠️ Nota**: La extracción automática de PDFs con tablas es compleja. Este extractor es experimental.

```bash
# Instalar dependencia
pip install PyPDF2

# Intentar extracción
python pdf_to_json.py "Stundenplan der Klasse 7d.pdf" --output 7d.json -v
```

Para mejores resultados con PDFs complejos:
```bash
pip install pdfplumber
```

**Recomendación**: Para horarios existentes, usa el **asistente interactivo** (Opción 1) o la **creación manual** (Opción 2).

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

## 🐛 Solución de problemas

Si tienes problemas al importar los archivos .ics:

1. **Verifica formato JSON**: Asegúrate de que los archivos JSON estén correctamente formateados
2. **Usa modo verbose**: Ejecuta con `--verbose` para ver información detallada
3. **Valida archivos .ics**: Usa https://icalendar.org/validator.html antes de importar
4. **Prueba otros clientes**: Si Google Calendar falla, intenta con Apple Calendar u Outlook
5. **Revisa logs**: El script proporciona mensajes de error detallados

### Errores comunes

- **"Archivo no encontrado"**: Verifica que los archivos `7d.json` y `7e.json` existan en el directorio de entrada
- **"Evento X fuera de rango"**: Revisa que los días estén entre 1-5 y los períodos entre 1-12
- **"Faltan campos requeridos"**: Cada evento debe tener `dia`, `periodo`, `asignatura` y `aula`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Lacomax** - [GitHub](https://github.com/Lacomax)

## 🙏 Agradecimientos

- KKG (Käthe-Kollwitz-Gymnasium) por los horarios escolares
- Comunidad de Python por las herramientas y librerías
- Todos los contribuidores del proyecto

## 🔗 Integración con SubstituteFinder

Este proyecto se integra perfectamente con [SubstituteFinder](https://github.com/Lacomax/SubstituteFinder), un sistema de monitoreo automático de sustituciones escolares.

### ¿Cómo funciona la integración?

```
┌─────────────────────────────────────────────────────────────┐
│                    Flujo de Trabajo                         │
└─────────────────────────────────────────────────────────────┘

1. 📄 PDF Horario Escolar
        │
        ↓ (pdf_to_json.py)
2. 📋 Archivos JSON (7d.json, 7e.json)
        │
        ├─→ 📅 KKGStundenplan2Google (main.py)
        │       └─→ calendario_7d.ics, calendario_7e.ics
        │           └─→ Google Calendar / Apple Calendar
        │
        └─→ 🔍 SubstituteFinder (dsb_finder.py)
                └─→ Monitorea DSB y detecta cambios
                    └─→ Notificaciones de sustituciones
```

### Archivos JSON compartidos

Ambos proyectos utilizan el **mismo formato JSON**:

```json
{
  "clase": "7d",
  "eventos": [
    {
      "dia": 1,
      "periodo": 1,
      "asignatura": "m",
      "aula": "A104"
    }
  ]
}
```

### Configuración de ambos repos

**Paso 1**: Genera los JSON desde PDF (en este repo)
```bash
python pdf_to_json.py "Stundenplan der Klasse 7d.pdf" --output 7d.json
python pdf_to_json.py "Stundenplan der Klasse 7e.pdf" --output 7e.json
```

**Paso 2**: Genera calendarios ICS (en este repo)
```bash
python main.py
```

**Paso 3**: Copia los JSON a SubstituteFinder
```bash
cp 7d.json 7e.json ../SubstituteFinder/data/
```

**Paso 4**: Ejecuta SubstituteFinder para monitorear sustituciones
```bash
cd ../SubstituteFinder
python dsb_finder.py
```

### Beneficios de la integración

- ✅ **Consistencia**: Un solo archivo JSON para ambos sistemas
- ✅ **Actualización fácil**: Cambia el PDF → actualiza JSON → ambos repos sincronizados
- ✅ **Workflow completo**: Desde PDF hasta calendario + monitoreo de sustituciones

### Ejemplo completo

```bash
# 1. Clonar ambos repositorios
git clone https://github.com/Lacomax/KKGStundenplan2Google.git
git clone https://github.com/Lacomax/SubstituteFinder.git

# 2. Generar JSON desde PDF
cd KKGStundenplan2Google
python pdf_to_json.py "Stundenplan der Klasse 7d.pdf" -o 7d.json

# 3. Generar calendario
python main.py

# 4. Compartir JSON con SubstituteFinder
cp 7d.json 7e.json ../SubstituteFinder/data/

# 5. Importar calendario a Google Calendar
# (manualmente o usando la API de Google Calendar)

# 6. Monitorear sustituciones
cd ../SubstituteFinder
python dsb_finder.py
```

## 📞 Contacto

Si tienes preguntas o sugerencias, por favor abre un issue en GitHub.

## 🔗 Proyectos Relacionados

- [SubstituteFinder](https://github.com/Lacomax/SubstituteFinder) - Monitoreo automático de sustituciones escolares DSB

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!