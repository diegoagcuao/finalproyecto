from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, Link
from app import database as db
from app.utils import extraer_informacion_enlace
import pickle
from datetime import datetime

links_blueprint = Blueprint('links', __name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@links_blueprint.route('/')
@login_required
def home():
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.fecha_procesamiento.desc()).all()
    return render_template('index.html', links=links)

@links_blueprint.route('/procesar_link', methods=['POST'])
@login_required
def procesar_link():
    enlace = request.form.get('enlace')

    # Verificar si el enlace ya existe para el usuario actual
    enlace_existente = Link.query.filter_by(enlace=enlace, user_id=current_user.id).first()
    
    if enlace_existente:
        flash("Ya has guardado este enlace anteriormente.", "danger")
        return redirect(url_for('links.home'))  # Redirigir a la página principal si el enlace ya existe

    # Extraer información del enlace (título, descripción, imagen)
    titulo, descripcion, imagen = extraer_informacion_enlace(enlace)
    text = titulo + ' ' + descripcion
    X = vectorizer.transform([text])
    categoria = model.predict(X)[0]

    # Crear un nuevo enlace si no existe
    nuevo_link = Link(enlace=enlace, titulo=titulo, descripcion=descripcion, imagen=imagen, categoria=categoria, user_id=current_user.id,fecha_procesamiento=datetime.utcnow())
    db.session.add(nuevo_link)
    db.session.commit()

    flash("Enlace guardado correctamente.", "success")
    return redirect(url_for('links.home'))

@links_blueprint.route('/eliminar_link/<int:id>', methods=['POST'])
@login_required
def eliminar_link(id):
    link = Link.query.get_or_404(id)
    if link.user_id != current_user.id:
        return redirect(url_for('links.home'))
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for('links.home'))
