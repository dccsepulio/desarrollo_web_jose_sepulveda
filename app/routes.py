from flask import render_template
from app import app
from app.models import Actividad

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agregar")
def agregar_actividad():
    return render_template("agregar_actividad.html")


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")

@app.route("/actividades")
def listado_actividades():
    actividades = Actividad.query.order_by(Actividad.inicio.desc()).limit(5).all()
    return render_template("listado_actividades.html", actividades=actividades)

@app.route("/actividad/<int:id>")
def ver_actividad(id):
    return render_template("ver_actividad.html", actividad_id=id)