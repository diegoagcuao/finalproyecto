from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import database as db

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('El nombre de usuario ya está registrado.', 'danger')
            return redirect(url_for('users.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso, ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('users.login'))

        login_user(user)
        flash('Has iniciado sesión con éxito.', 'success')
        return redirect(url_for('links.home'))

    return render_template('login.html')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('users.login'))
