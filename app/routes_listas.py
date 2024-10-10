from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app import database as db
from app.models import Lista, EnlaceLista, Link, ListaCompartida, User

listas_blueprint = Blueprint('listas', __name__)

# Ruta para ver las listas del usuario en formato acordeón
@listas_blueprint.route('/mis_listas')
@login_required
def mis_listas():
    # Listas creadas por el usuario
    listas = Lista.query.filter_by(user_id=current_user.id).all()

    # Listas compartidas con el usuario actual
    listas_compartidas = ListaCompartida.query.filter_by(user_id=current_user.id).all()

    return render_template('mis_listas.html', listas=listas, listas_compartidas=[lista.lista for lista in listas_compartidas])


# Ruta para ver una lista compartida con el usuario
@listas_blueprint.route('/ver_lista_compartida/<int:lista_id>', methods=['GET'])
@login_required
def ver_lista_compartida(lista_id):
    lista = Lista.query.get_or_404(lista_id)
    lista_compartida = ListaCompartida.query.filter_by(lista_id=lista.id, user_id=current_user.id).first()
    if not lista_compartida:
        flash("No tienes permiso para ver esta lista.", "danger")
        return redirect(url_for('listas.mis_listas'))

    enlaces = EnlaceLista.query.filter_by(lista_id=lista.id).all()
    return render_template('ver_lista_compartida.html', lista=lista, enlaces=enlaces)


# Ruta para obtener los enlaces de una lista específica usando AJAX
@listas_blueprint.route('/obtener_enlaces_lista/<int:lista_id>', methods=['GET'])
@login_required
def obtener_enlaces_lista(lista_id):
    enlaces = EnlaceLista.query.filter_by(lista_id=lista_id).all()
    enlaces_dict = [{"titulo": enlace.link.titulo, "href": enlace.link.enlace, "categoria": enlace.link.categoria, "id": enlace.id} for enlace in enlaces]
    return jsonify(enlaces_dict)


# Ruta para eliminar un enlace de una lista sin eliminarlo de la tabla general de enlaces
@listas_blueprint.route('/eliminar_enlace_lista', methods=['POST'])
@login_required
def eliminar_enlace_lista():
    enlace_lista_id = request.form.get('enlace_lista_id')
    enlace_lista = EnlaceLista.query.get_or_404(enlace_lista_id)
    
    db.session.delete(enlace_lista)
    db.session.commit()
    return jsonify({"message": "Enlace eliminado de la lista correctamente"})


# Ruta para crear una nueva lista
@listas_blueprint.route('/crear_lista', methods=['GET', 'POST'])
@login_required
def crear_lista():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        # Verificar si ya existe una lista con el mismo nombre para este usuario
        lista_existente = Lista.query.filter_by(user_id=current_user.id, nombre=nombre).first()
        if lista_existente:
            flash('Ya tienes una lista con ese nombre. Por favor, elige un nombre diferente.', 'danger')
            return redirect(url_for('listas.crear_lista'))

        nueva_lista = Lista(nombre=nombre, descripcion=descripcion, user_id=current_user.id)
        db.session.add(nueva_lista)
        db.session.commit()
        flash('Lista creada correctamente', 'success')
        return redirect(url_for('listas.mis_listas'))

    return render_template('crear_lista.html')


# Ruta para eliminar una lista
@listas_blueprint.route('/eliminar_lista/<int:lista_id>', methods=['POST'])
@login_required
def eliminar_lista(lista_id):
    lista = Lista.query.get_or_404(lista_id)
    if lista.user_id != current_user.id:
        flash("No tienes permiso para eliminar esta lista", "danger")
        return redirect(url_for('listas.mis_listas'))

    # Eliminar todos los enlaces asociados a la lista
    EnlaceLista.query.filter_by(lista_id=lista_id).delete()
    db.session.delete(lista)
    db.session.commit()
    flash("Lista eliminada correctamente", "success")
    return redirect(url_for('listas.mis_listas'))


# Nueva vista para compartir una lista con otros usuarios y gestionar permisos
@listas_blueprint.route('/compartir_lista/<int:lista_id>', methods=['GET', 'POST'])
@login_required
def compartir_lista(lista_id):
    lista = Lista.query.get_or_404(lista_id)

    if request.method == 'POST':
        username = request.form.get('username')
        usuario_a_compartir = User.query.filter_by(username=username).first()

        if usuario_a_compartir:
            # Verificar si la lista ya ha sido compartida con este usuario
            lista_compartida = ListaCompartida.query.filter_by(lista_id=lista.id, user_id=usuario_a_compartir.id).first()
            if lista_compartida:
                flash(f"Ya has compartido esta lista con {usuario_a_compartir.username}.", "danger")
                return redirect(url_for('listas.compartir_lista', lista_id=lista.id))

            # Validar que el usuario no se comparta la lista a sí mismo
            if usuario_a_compartir.id == current_user.id:
                flash('No puedes compartir una lista contigo mismo.', 'danger')
                return redirect(url_for('listas.compartir_lista', lista_id=lista.id))

            # Crear una nueva entrada en ListaCompartida
            nueva_comparticion = ListaCompartida(lista_id=lista.id, user_id=usuario_a_compartir.id)
            db.session.add(nueva_comparticion)
            db.session.commit()
            flash(f"Lista compartida con {usuario_a_compartir.username}.", 'success')
        else:
            flash(f"Usuario {username} no encontrado.", 'danger')

        return redirect(url_for('listas.compartir_lista', lista_id=lista.id))

    # Obtener todos los usuarios con los que se ha compartido la lista
    usuarios_compartidos = ListaCompartida.query.filter_by(lista_id=lista.id).all()
    return render_template('compartir_lista.html', lista=lista, usuarios_compartidos=usuarios_compartidos)


# Ruta para eliminar el permiso de compartir lista con un usuario específico
@listas_blueprint.route('/eliminar_compartir_lista/<int:lista_id>/<int:user_id>', methods=['POST'])
@login_required
def eliminar_compartir_lista(lista_id, user_id):
    # Buscar la relación de lista compartida
    lista_compartida = ListaCompartida.query.filter_by(lista_id=lista_id, user_id=user_id).first()

    if not lista_compartida:
        flash("No se encontró la relación de compartir lista.", "danger")
        return redirect(url_for('listas.compartir_lista', lista_id=lista_id))
    
    # Eliminar la relación
    db.session.delete(lista_compartida)
    db.session.commit()
    flash("Se ha eliminado el acceso a la lista compartida.", "success")
    
    return redirect(url_for('listas.compartir_lista', lista_id=lista_id))


@listas_blueprint.route('/eliminar_lista_compartida/<int:lista_id>', methods=['POST'])
@login_required
def eliminar_lista_compartida(lista_id):
    lista_compartida = ListaCompartida.query.filter_by(lista_id=lista_id, user_id=current_user.id).first()
    if lista_compartida:
        db.session.delete(lista_compartida)
        db.session.commit()
        flash("Has eliminado la lista compartida.", "success")
    return redirect(url_for('listas.mis_listas'))



# Ruta para obtener las listas del usuario en formato JSON (usada para AJAX)
'''
@listas_blueprint.route('/obtener_listas', methods=['GET'])
@login_required
def obtener_listas():
    listas = Lista.query.filter_by(user_id=current_user.id).all()
    listas_dict = [{"id": lista.id, "nombre": lista.nombre} for lista in listas]
    return jsonify({"listas": listas_dict})
'''

@listas_blueprint.route('/obtener_listas/<int:enlace_id>', methods=['GET'])
@login_required
def obtener_listas(enlace_id):
    # Obtener las listas en las que ya está el enlace
    listas_con_enlace = EnlaceLista.query.filter_by(link_id=enlace_id).with_entities(EnlaceLista.lista_id).all()
    listas_con_enlace_ids = [lista.lista_id for lista in listas_con_enlace]

    # Obtener todas las listas del usuario, excluyendo las que ya contienen el enlace
    listas = Lista.query.filter(Lista.user_id == current_user.id, Lista.id.notin_(listas_con_enlace_ids)).all()

    # Convertir las listas a un formato JSON adecuado para la respuesta
    listas_json = [{'id': lista.id, 'nombre': lista.nombre} for lista in listas]
    return jsonify(listas_json)

def obtener_listas(enlace_id):
    # Obtener las listas en las que ya está el enlace
    listas_con_enlace = EnlaceLista.query.filter_by(link_id=enlace_id).with_entities(EnlaceLista.lista_id).all()
    listas_con_enlace_ids = [lista.lista_id for lista in listas_con_enlace]

    # Obtener todas las listas del usuario, excluyendo las que ya contienen el enlace
    listas = Lista.query.filter(Lista.user_id == current_user.id, Lista.id.notin_(listas_con_enlace_ids)).all()

    # Convertir las listas a un formato JSON adecuado para la respuesta
    listas_dict = [{'id': lista.id, 'nombre': lista.nombre} for lista in listas]
    return jsonify({"listas": listas_dict})

# Ruta para agregar un enlace a una lista
@listas_blueprint.route('/agregar_enlace_a_lista_ajax', methods=['POST'])
@login_required
def agregar_enlace_a_lista_ajax():
    lista_id = request.form.get('lista_id')
    enlace_id = request.form.get('enlace_id')
    nuevo_enlace_lista = EnlaceLista(lista_id=lista_id, link_id=enlace_id)
    db.session.add(nuevo_enlace_lista)
    db.session.commit()
    return jsonify({"message": "Enlace agregado a la lista correctamente"})


@listas_blueprint.route('/agregar_enlaces_a_lista/<int:lista_id>', methods=['GET', 'POST'])
@login_required
def agregar_enlaces_a_lista(lista_id):
    lista = Lista.query.get_or_404(lista_id)

    if request.method == 'POST':
        enlaces_ids = request.form.getlist('enlace_id')
        for enlace_id in enlaces_ids:
            nuevo_enlace_lista = EnlaceLista(lista_id=lista_id, link_id=int(enlace_id))
            db.session.add(nuevo_enlace_lista)
        db.session.commit()
        return redirect(url_for('listas.mis_listas'))

    # Obtener los IDs de los enlaces que ya están en la lista
    enlaces_en_lista = EnlaceLista.query.filter_by(lista_id=lista_id).with_entities(EnlaceLista.link_id).all()
    enlaces_en_lista_ids = [enlace.link_id for enlace in enlaces_en_lista]

    # Obtener todos los enlaces del usuario, excluyendo los que ya están en la lista
    links = Link.query.filter(Link.user_id == current_user.id, Link.id.notin_(enlaces_en_lista_ids)).all()

    return render_template('agregar_enlaces_a_lista.html', lista=lista, links=links)