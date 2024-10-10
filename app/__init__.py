from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


# Renombrar db a database
database = SQLAlchemy()

# Inicializar LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos y el sistema de login
    database.init_app(app)  # Cambiado a 'database'

    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = None

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes_users import users_blueprint
    from .routes_links import links_blueprint
    from .routes_listas import listas_blueprint

    app.register_blueprint(users_blueprint, url_prefix='/')
    app.register_blueprint(links_blueprint, url_prefix='/')
    app.register_blueprint(listas_blueprint, url_prefix='/')

    return app
