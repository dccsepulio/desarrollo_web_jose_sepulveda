from sqlalchemy import  Column, BigInteger, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

db = SQLAlchemy()

# --- Models ---

class ActividadTema(db.Model):
    __tablename__ = 'actividad_tema'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(BigInteger, ForeignKey('region.id'), nullable=False)

class ContactarPor(db.Model):
    __tablename__ = 'contactar_por'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)

class Foto(db.Model):
    __tablename__ = 'foto'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)

class Region(db.Model):
    __tablename__ = 'region'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

class Actividad(db.Model):
    __tablename__ = 'actividad'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    comuna_id = Column(BigInteger, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=True)
    descripcion = Column(String(500), nullable=False)

    comuna = relationship('Comuna')
    temas = relationship('ActividadTema', cascade='all, delete-orphan')
    contactos = relationship('ContactarPor', cascade='all, delete-orphan')
    fotos = relationship('Foto', cascade='all, delete-orphan')

# --- Database Functions ---