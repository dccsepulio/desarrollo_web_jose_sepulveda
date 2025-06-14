from flask import Blueprint, render_template, jsonify, request
from sqlalchemy.orm import joinedload
from sqlalchemy import func, extract, case
from ..database.db import db, Actividad, Comuna, Region, ActividadTema, ContactarPor, Foto, Comentario
from ..forms import ComentarioForm

bp = Blueprint('main', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=str(error)), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', error=str(error)), 500

@bp.route("/forzar-error") 
def forzar_error():
    raise Exception("Este es un error forzado para probar el 500.html")

@bp.route('/')
def index():
    ultimas = (Actividad.query
               .options(joinedload(Actividad.temas))   
               .order_by(Actividad.id.desc())
               .limit(5).all())
    return render_template('index.html', actividades=ultimas)

@bp.route('/actividades')
def listado_actividades():
    page = request.args.get('page', 1, type=int)
    pager = (Actividad.query
             .options(joinedload(Actividad.temas)) 
             .order_by(Actividad.id.desc())
             .paginate(page=page, per_page=5, error_out=False))
    return render_template('listado_actividades.html',
                           actividades=pager.items, pagination=pager)

@bp.route('/actividad/<int:actividad_id>')
def ver_actividad(actividad_id: int):
    actividad = (Actividad.query
                 .options(
                     joinedload(Actividad.temas),
                     joinedload(Actividad.contactos),
                     joinedload(Actividad.fotos),
                     joinedload(Actividad.comuna).joinedload(Comuna.region) 
                 )
                 .get_or_404(actividad_id))
    return render_template('ver_actividad.html', actividad=actividad, comentario_form=ComentarioForm())

@bp.route('/estadisticas')
def estadisticas():
    """Stub temporal: se implementará en la Tarea 3."""
    return render_template('estadisticas.html')

@bp.route('/api/comunas')
def api_comunas():
    region_id = request.args.get('region_id', type=int)
    comunas = (Comuna.query
               .filter_by(region_id=region_id)
               .order_by(Comuna.nombre)
               .all())
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])
    
@bp.route('/api/estadisticas')
def api_estadisticas():
    # 1) línea: actividades por día
    linea = (db.session
             .query(func.date(Actividad.dia_hora_inicio).label('dia'),
                    func.count().label('total'))
             .group_by('dia')
             .order_by('dia')
             .all())
    datos_linea = [{'dia': str(d.dia), 'total': d.total} for d in linea]

    # 2) torta: total por tipo  (cuenta los temas declarados)
    torta = (db.session
             .query(ActividadTema.tema, func.count().label('total'))
             .group_by(ActividadTema.tema)
             .all())
    datos_torta = [{'tema': t.tema, 'total': t.total} for t in torta]

    # 3) barras: mañana/mediodía/tarde por mes (YYYY-MM)
    h = extract('hour', Actividad.dia_hora_inicio)
    barras = (db.session
              .query(func.date_format(Actividad.dia_hora_inicio, '%Y-%m').label('mes'),
                     func.sum(case((h.between(6, 11), 1), else_=0)).label('manana'),
                     func.sum(case((h.between(12, 14), 1), else_=0)).label('mediodia'),
                     func.sum(case((h.between(15, 20), 1), else_=0)).label('tarde'))
              .group_by('mes').order_by('mes')
              .all())
    datos_barras = [{
        'mes':      b.mes,
        'manana':   int(b.manana or 0),
        'mediodia': int(b.mediodia or 0),
        'tarde':    int(b.tarde or 0)
    } for b in barras]

    return jsonify({'line': datos_linea,
                    'pie':  datos_torta,
                    'bar':  datos_barras})

@bp.route('/api/actividad/<int:actividad_id>/comentarios', methods=['GET'])
def api_obtener_comentarios(actividad_id):
    comentarios = (Comentario.query
                   .filter_by(actividad_id=actividad_id)
                   .order_by(Comentario.fecha.desc())
                   .all())
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'texto':  c.texto,
        'fecha':  c.fecha.strftime('%Y-%m-%d %H:%M')
    } for c in comentarios])

@bp.route('/api/actividad/<int:actividad_id>/comentarios', methods=['POST'])
def api_agregar_comentario(actividad_id):
    form = ComentarioForm()
    if not form.validate_on_submit(): # valida en servidor
        return jsonify({'ok': False, 'errors': form.errors}), 400

    nuevo = Comentario(actividad_id=actividad_id,
                       nombre=form.nombre.data,
                       texto=form.texto.data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'ok': True})