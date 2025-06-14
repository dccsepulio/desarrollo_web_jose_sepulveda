import os
from pathlib import Path 
from flask import (
    Blueprint, render_template, flash, redirect, url_for,
    request, current_app
)
from werkzeug.utils import secure_filename
from ..forms import ActividadForm
from ..database.db import (
    db, Region, Comuna, Actividad, ActividadTema,
    ContactarPor, Foto
)

bp = Blueprint('actividad', __name__)

# Helpers

def _cargar_selects(form: ActividadForm) -> None:
    form.region.choices = [
        (r.id, r.nombre) for r in Region.query.order_by(Region.nombre)
    ]
    comunas = (Comuna.query
               .filter_by(region_id=form.region.data or 0)
               .order_by(Comuna.nombre))
    form.comuna.choices = [(c.id, c.nombre) for c in comunas]

def _extraer_contactos():
    nombres = request.form.getlist('contact_nombre[]')
    ids     = request.form.getlist('contact_id[]')
    for nom, ide in zip(nombres, ids):
        if nom and ide:
            yield nom, ide

@bp.app_template_filter("listar_temas")
def listar_temas(temas):
    etiquetas = []
    for t in temas:
        if t.tema == "otro":
            etiquetas.append(f"Otro ({t.glosa_otro})")
        else:
            etiquetas.append(t.tema.capitalize())
    return ", ".join(etiquetas)

# Vista principal 

@bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = ActividadForm()
    _cargar_selects(form) 
    regiones = Region.query.order_by(Region.nombre).all()

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Revise los errores del formulario', 'danger')
            return render_template('agregar_actividad.html', form=form, regiones=regiones )

        try:
            act = Actividad(
                comuna_id         = form.comuna.data,
                sector            = form.sector.data or None,
                nombre            = form.nombre.data,
                email             = form.email.data,
                celular           = form.celular.data or None,
                dia_hora_inicio   = form.inicio.data,
                dia_hora_termino  = form.termino.data,
                descripcion       = form.descripcion.data or ''
            )
            db.session.add(act)
            db.session.flush()

            # Temas
            for tema in form.temas.data:
                db.session.add(ActividadTema(
                    tema        = tema,
                    glosa_otro  = form.glosa_otro.data if tema == 'otro' else None,
                    actividad_id= act.id
                ))

            # Contactos dinámicos
            for medio, identificador in _extraer_contactos():
                db.session.add(ContactarPor(
                    nombre        = medio,
                    identificador = identificador,
                    actividad_id  = act.id
                ))

            # Fotos (1–5)
            archivos = request.files.getlist('fotos') 
            if not 1 <= len(archivos) <= 5:
                raise ValueError('Debe subir entre 1 y 5 imágenes')

            if not 1 <= len(archivos) <= 5:
                raise ValueError('Debe subir entre 1 y 5 imágenes')

            for archivo in archivos:
                if archivo.filename == '':
                    continue
                filename = secure_filename(archivo.filename)
                uploads_root = Path(current_app.root_path) / 'static' / current_app.config['UPLOAD_FOLDER']
                ruta_abs = uploads_root / filename
                archivo.save(ruta_abs)

                db.session.add(Foto(
                    ruta_archivo   = ruta_abs.relative_to(Path(current_app.root_path) / 'static').as_posix(),
                    nombre_archivo = filename,
                    actividad_id   = act.id
                ))

            db.session.commit()
            flash("Actividad registrada correctamente.", "success")
            return redirect(url_for('main.index'))

        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash('Ocurrió un error al guardar la actividad.', 'danger')

    # GET
    return render_template('agregar_actividad.html', form=form, regiones=regiones )