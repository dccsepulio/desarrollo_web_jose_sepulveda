# desarrollo_web_jose_sepulveda Tarea 2  
Aplicación Flask + MySQL que transforma el prototipo de la Tarea 1 en un sistema funcional con persistencia.

## Actividades Recreativas — Implementación back-end

Incluye:
- **Portada**: últimas 5 actividades recién creadas.
- **Formulario “Agregar actividad”**  
  * Validaciones JavaScript + validaciones servidor-side con WTForms.  
  * Subida de entre 1 y 5 fotos; se almacenan en `static/uploads/`.
- **Listado**: paginación de 5 en 5; clic → detalle.
- **Detalle**: muestra todos los datos, contactos y galería flexible (sin bullets).
- **API auxiliar**: `/api/comunas?region_id=<id>` para autocompletar el combo de comunas.
- **Datos demo**: once actividades pre-cargadas con organizador, tema y foto.

### Decisiones de diseño
- **SQLAlchemy + Blueprints**: fácil de extender en T3 (estadísticas).
- **ENUM limpio en utf8mb4**: se ejecuta el `.sql` con `--default-character-set=utf8mb4` para evitar mojibake.
- **Rutas de foto relativas** : hay una carpeta img/ que se conserva de tarea1
- **Filtro Jinja `listar_temas`**: “Otro (Cultura)” cuando el tema es `otro`.
- **Mensajes flash** para feedback; overlay JS solo para previsualizar fotos, no para alerta final.

### Estructura para la tarea 2
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
│   │   └── region-comuna.sql
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── agregar_actividad.html
│   │   ├── listado_actividades.html
│   │   ├── estadisticas.html
│   │   └── ver_actividad.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
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

### Validación
- Probado en Python 3.12, Flask 3.0 y MySQL 8.0.
- HTML 5 y CSS 3 verificados con el validador W3C.
- Navegadores: Chrome 126, Firefox 127 en 1920 × 1080 y 1366 × 768.