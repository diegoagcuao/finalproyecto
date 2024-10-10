from app import database as db  # Cambiado a 'database'
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    listas = db.relationship('Lista', backref='creador', lazy=True, cascade="all, delete-orphan")

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enlace = db.Column(db.String(500), nullable=False)
    titulo = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.String(500), nullable=True)
    imagen = db.Column(db.String(500), nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relación con EnlaceLista con borrado en cascada
    enlaces_listas = db.relationship('EnlaceLista', backref='link', cascade="all, delete-orphan")
    fecha_procesamiento = db.Column(db.DateTime, default=datetime.utcnow)


class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relación con EnlaceLista con borrado en cascada
    enlaces = db.relationship('EnlaceLista', backref='lista', cascade="all, delete-orphan")
    # Relación con usuarios con los que se comparte la lista
    compartida_con = db.relationship('ListaCompartida', backref='lista', cascade="all, delete-orphan")
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    # Agregar la relación con el modelo User
    usuario = db.relationship('User', backref=db.backref('creador_de_lista', lazy=True))


class EnlaceLista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lista_id = db.Column(db.Integer, db.ForeignKey('lista.id', ondelete="CASCADE"), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id', ondelete="CASCADE"), nullable=False)

# Renombrado a ListaCompartida, eliminando el concepto de permisos
class ListaCompartida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lista_id = db.Column(db.Integer, db.ForeignKey('lista.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    # Relación para acceder a los datos del usuario con el que se compartió la lista
    usuario = db.relationship('User', backref='listas_compartidas')

