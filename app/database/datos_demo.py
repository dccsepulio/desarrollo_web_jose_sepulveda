from datetime import datetime
from pathlib import Path
from itertools import count

from app import app, db
from app.database.db import Actividad, ActividadTema, Comuna, Foto

fmt = "%Y-%m-%d %H:%M"

# Lista de actividades con nombres de comuna
BASE_ACTIVIDADES = [
    {
        "inicio": "2025-04-15 10:00", "termino": "2025-04-15 12:00",
        "comuna_nombre": "Puente Alto", "sector": "Cancha central",
        "nombre": "Carolina Pizarro", "tema": "ciencias", "glosa_otro": None,
        "email": "pintura@example.com", "celular": "912345683",
        "descripcion": "Actividad artística para niños", "foto": "foto6.jpg"
    },
    {
        "inicio": "2025-04-18 15:00", "termino": "2025-04-18 16:30",
        "comuna_nombre": "Recoleta", "sector": "Centro comunitario",
        "nombre": "Fundación Verde", "tema": "tecnologia", "glosa_otro": None,
        "email": "compost@example.com", "celular": "912345684",
        "descripcion": "Aprende a compostar en casa", "foto": "foto7.jpg"
    },
    {
        "inicio": "2025-04-20 17:00", "termino": "2025-04-20 18:00",
        "comuna_nombre": "Maipú", "sector": "Plaza de armas",
        "nombre": "Yoga Maipú", "tema": "baile", "glosa_otro": None,
        "email": "yoga@example.com", "celular": "912345685",
        "descripcion": "Relájate y estírate al aire libre", "foto": "foto8.jpg"
    },
    {
        "inicio": "2025-04-22 19:00", "termino": "2025-04-22 20:30",
        "comuna_nombre": "Las Condes", "sector": "Centro cultural",
        "nombre": "Municipalidad", "tema": "otro", "glosa_otro": "Cultura",
        "email": "libros@example.com", "celular": "912345686",
        "descripcion": "Conversatorio con autores locales", "foto": "foto9.jpg"
    },
    {
        "inicio": "2025-04-25 08:00", "termino": "2025-04-25 09:30",
        "comuna_nombre": "Macul", "sector": "Calle peatonal",
        "nombre": "Municipalidad", "tema": "comida", "glosa_otro": None,
        "email": "salud@example.com", "celular": "912345687",
        "descripcion": "Exposición de productos saludables", "foto": "foto10.jpg"
    },
    {
        "inicio": "2025-04-27 14:00", "termino": "2025-04-27 15:30",
        "comuna_nombre": "Independencia", "sector": "Estadio municipal",
        "nombre": "Escuela de boxeo", "tema": "deporte", "glosa_otro": None,
        "email": "futbol@example.com", "celular": "912345688",
        "descripcion": "Competencia deportiva abierta", "foto": "foto11.jpg"
    },
    {
        "inicio": "2025-03-28 12:00", "termino": "2025-03-28 14:00",
        "comuna_nombre": "Santiago", "sector": "Beauchef 850, terraza",
        "nombre": "Fake name 1", "tema": "deporte", "glosa_otro": None,
        "email": "boxeo@example.com", "celular": "912345678",
        "descripcion": "Entrenamiento básico de boxeo", "foto": "foto1.jpg"
    },
    {
        "inicio": "2025-03-29 19:00", "termino": "2025-03-29 20:00",
        "comuna_nombre": "Ñuñoa", "sector": "Plaza",
        "nombre": "Fake name 2", "tema": "ciencias", "glosa_otro": None,
        "email": "fruta@example.com", "celular": "912345679",
        "descripcion": "Charla sobre deshidratación de fruta", "foto": "foto2.jpg"
    },
    {
        "inicio": "2025-03-30 18:00", "termino": None,
        "comuna_nombre": "Santiago", "sector": "Parque O´Higgins",
        "nombre": "Fake name 3", "tema": "música", "glosa_otro": None,
        "email": "musica@example.com", "celular": "912345680",
        "descripcion": "Evento musical urbano", "foto": "foto3.jpg"
    },
    {
        "inicio": "2025-04-01 09:30", "termino": "2025-04-01 11:00",
        "comuna_nombre": "La Florida", "sector": "Gimnasio Municipal",
        "nombre": "Fake name 4", "tema": "deporte", "glosa_otro": None,
        "email": "zumba@example.com", "celular": "912345681",
        "descripcion": "Sesión de zumba para todos", "foto": "foto4.jpg"
    },
    {
        "inicio": "2025-04-12 16:00", "termino": "2025-04-12 19:00",
        "comuna_nombre": "Providencia", "sector": "Café al aire libre",
        "nombre": "Fake name 5", "tema": "tecnologia", "glosa_otro": None,
        "email": "tec@example.com", "celular": "912345682",
        "descripcion": "Hablamos sobre avances tecnológicos", "foto": "foto5.jpg"
    }
]

UPLOAD_SUBDIR = "img"
(Path(app.root_path) / "static" / UPLOAD_SUBDIR).mkdir(parents=True, exist_ok=True)

with app.app_context():
    for dato in BASE_ACTIVIDADES:
        comuna = (
            Comuna.query
            .filter(Comuna.nombre.ilike(f"%{dato['comuna_nombre']}%"))
            .first()
        )
        if not comuna:
            print(f"Comuna '{dato['comuna_nombre']}' no encontrada. Omitida.")
            continue

        # Evita duplicados
        existente = (
            Actividad.query.filter_by(
                nombre=dato["nombre"],
                dia_hora_inicio=datetime.strptime(dato["inicio"], fmt)
            ).first()
        )
        if existente:
            print(f"Actividad con misma fecha+organizador ya existe. Omitida.")
            continue

        actividad = Actividad(
            comuna_id       = comuna.id,
            sector          = dato["sector"],
            nombre          = dato["nombre"],        # ← organizador
            email           = dato["email"],
            celular         = dato["celular"],
            dia_hora_inicio = datetime.strptime(dato["inicio"], fmt),
            dia_hora_termino= (datetime.strptime(dato["termino"], fmt)
                               if dato["termino"] else None),
            descripcion     = dato["descripcion"],
        )
        db.session.add(actividad)
        db.session.flush()        # obtiene actividad.id

        # Foto
        ruta_rel = f"{UPLOAD_SUBDIR}/{dato['foto']}"
        db.session.add(
            Foto(
                ruta_archivo   = ruta_rel,
                nombre_archivo = dato["foto"],
                actividad_id   = actividad.id,
            )
        )

        # Tema principal
        db.session.add(
            ActividadTema(
                tema         = dato["tema"],
                glosa_otro   = dato.get("glosa_otro"),
                actividad_id = actividad.id,
            )
        )

    db.session.commit()
    print("Datos cargados exitosamente.")