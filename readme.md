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
- No requiere dependencias externas (solo biblioteca estándar)

## Estructura del Proyecto

- `main.py`: Script principal para generar calendarios ICS
- `7d.json`: Datos para la clase 7d (Diego)
- `7e.json`: Datos para la clase 7e (Mateo)
- `output/`: Carpeta donde se guardan los calendarios ICS generados
  - `calendario_7d.ics`: Calendario para Diego (clase 7d)
  - `calendario_7e.ics`: Calendario para Mateo (clase 7e)

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

## 📞 Contacto

Si tienes preguntas o sugerencias, por favor abre un issue en GitHub.

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!