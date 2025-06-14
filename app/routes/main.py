from flask import Blueprint, render_template, jsonify, request
from sqlalchemy.orm import joinedload
from ..database.db import db, Actividad, Comuna, Region, ActividadTema, ContactarPor, Foto

bp = Blueprint('main', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=str(error)), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', error=str(error)), 500

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
    return render_template('ver_actividad.html', actividad=actividad)

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
    
@bp.route("/forzar-error") 
def forzar_error():
    raise Exception("Este es un error forzado para probar el 500.html")