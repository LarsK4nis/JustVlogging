from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instancias de las extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuraciones básicas de la aplicación
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/microblogging'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa las extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)

    # Configurar el cargador de usuario para Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importa las rutas dentro del contexto de la aplicación
    with app.app_context():
        from . import routes
        db.create_all()  # Crea las tablas de la base de datos si no existen

    return app
