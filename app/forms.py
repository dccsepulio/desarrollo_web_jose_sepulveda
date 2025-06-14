from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, DateTimeField,
    SelectField, SelectMultipleField
)
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp 
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import TelField 
from flask_wtf.file import MultipleFileField 

class ActividadForm(FlaskForm):
    # Dónde
    region  = SelectField('Región',  coerce=int, validators=[DataRequired()])
    comuna  = SelectField('Comuna',  coerce=int, validators=[DataRequired()])
    sector  = StringField('Sector',  validators=[Optional(), Length(max=100)])

    # Quién
    nombre  = StringField('Organizador', validators=[DataRequired(), Length(max=200)])
    email   = StringField('Email',       validators=[DataRequired(), Email(), Length(max=100)])
    celular = StringField('Celular',     validators=[Optional(),
                                                    Regexp(r'^\+\d{1,3}\.\d{7,10}$',
                                                           message='Formato +569.12345678')])

    # Contactos dinámicos (se manejarán “a mano”, no van en WTForms)

    # Cuándo
    inicio  = DateTimeField('Inicio',  format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    termino = DateTimeField('Término', format='%Y-%m-%dT%H:%M', validators=[Optional()])

    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=500)])

    # Temas (SelectMultiple)
    temas = SelectMultipleField('Temas',
        coerce=str,
        choices=[('música','Música'), ('deporte','Deporte'),
                 ('ciencias','Ciencias'), ('religión','Religión'),
                 ('política','Política'), ('tecnología','Tecnología'),
                 ('juegos','Juegos'), ('baile','Baile'),
                 ('comida','Comida'), ('otro','Otro')],
        validators=[DataRequired()]
    )
    glosa_otro = StringField('Otro tema', validators=[Optional(), Length(min=3, max=15)])

    # Fotos
    fotos = MultipleFileField('Fotos (1–5)',
        validators=[
            DataRequired(message='Debe subir al menos una foto'),
            FileAllowed(['jpg','jpeg','png'], 'Solo imágenes JPG/PNG')
        ])

class ComentarioForm(FlaskForm):
    nombre = StringField('Nombre',  validators=[DataRequired(), Length(min=3, max=80)])
    texto  = TextAreaField('Comentario', validators=[DataRequired(), Length(min=5)])
