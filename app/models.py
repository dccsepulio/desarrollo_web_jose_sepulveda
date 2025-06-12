from app import db

class Actividad(db.Model):
    __tablename__ = "actividad"

    id = db.Column(db.Integer, primary_key=True)
    inicio = db.Column(db.DateTime, nullable=False)
    termino = db.Column(db.DateTime)
    comuna = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100))
    tema = db.Column(db.String(100), nullable=False)
    organizador = db.Column(db.String(200), nullable=False)
    total_fotos = db.Column(db.Integer)  # Esto puedes calcularlo aparte si quieres
