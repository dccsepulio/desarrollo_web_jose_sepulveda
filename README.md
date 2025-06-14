# desarrollo_web_jose_sepulveda Tarea 3
Aplicación Flask + MySQL que evoluciona la T2.
Ahora incluye estadísticas interactivas y comentarios asíncronos sobre cada actividad.

## Novedades de la T3

Incluye:
- **Estadísticas**: Highcharts + Fetch API (`/api/estadisticas`)
- **Comentarios**: Fetch API (`/api/actividad/<id>/comentarios`) + WTForms
- **Base de datos**: Nueva tabla comentario	SQLAlchemy ORM
- **Datos demo**: 20 actividades distribuidas en marzo-mayo con distintos horarios.


## Decisiones de diseño
- **XSS**: Jinja2 auto-escapa.
- **CSRF**: todos los formularios POST usan token de WTForms.
- **SQL-Injection**: ORM SQLAlchemy, consultas parametrizadas.
- **Highcharts CDN**: evita dependencias Python extra y es aceptado por el enunciado.
- **Fetch + Promises** (ES6) en lugar de XHR clásico—código más legible.
- **Agrupación horaria** en SQL con `HOUR()` y `CASE` → conteos exactos por franja.
- **Campos INT en JSON**: el backend castea a `int` para que Highcharts no reciba strings.
- **Sin reloads**: tanto gráficos como comentarios se cargan/actualizan con AJAX.

## Estructura para la tarea 2
```bash
/mi-proyecto
├── .venv/
│
├── app/
│   ├── routes/
│   │   ├── actividad.py
│   │   └── main.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── init_db.py
│   │   ├── datos_demo.py
│   │   ├── tarea2.sql
│   │   ├── region-comuna.sql
│   │   └── tabla-comentario.sql 
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── agregar_actividad.html
│   │   ├── listado_actividades.html
│   │   ├── estadisticas.html
│   │   └── ver_actividad.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── script.js
│   │   │   ├── estadisticas.js
│   │   │   └── comentarios.js
│   │   ├── img/
│   │   │   ├── foto1.jpg
│   │   │   └── ...
│   │   └── uploads/
│   │
│   ├── __init__.py
│   └── forms.py
│
├── requirements.txt
├── run.py
└── README.md
```

## Cómo usar

1. Crear entorno virtual.
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Installar dependencias.
```bash
pip install -r requirements.txt
```
# pip freeze > requirements.txt


3. Crear la base y poblar regiones/comunas.
```bash
mysql --default-character-set=utf8mb4 -u cc5002 -p < app\database\tarea2.sql
mysql --default-character-set=utf8mb4 -u cc5002 -p tarea2 < app\database\region-comuna.sql
mysql --default-character-set=utf8mb4 -u cc5002 -p tarea2 < app\database\tabla-comentario.sql
```
Nota: la contraseña esta en el enunciado

4. Cargar datos de ejemplo.
```bash
python -m app.database.datos_demo
```

5. Abrir app.
```bash
python run.py
```
Visitar http://localhost:5000

## Validación
- Probado en Python 3.12, Flask 3.0, SQLAlchemy 2.0 y MySQL 8.0.
- HTML 5 y CSS 3 verificados con el validador W3C.
- Navegadores: Chrome 126, Firefox 127 en 1920 × 1080 y 1366 × 768.