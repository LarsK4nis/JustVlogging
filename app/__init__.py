from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from minio import Minio

# Instancias de las extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuraciones básicas de la aplicación
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/microblogging'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de MinIO
    app.config['MINIO_ENDPOINT'] = 'minio:9000'  # Cambia según tu configuración
    app.config['MINIO_ACCESS_KEY'] = 'minioadmin'  # Cambia por tu clave de acceso real
    app.config['MINIO_SECRET_KEY'] = 'minioadmin'  # Cambia por tu clave secreta real
    app.config['MINIO_SECURE'] = False  # Cambia a True si usas HTTPS
    app.config['MINIO_BUCKET'] = 'mybucket'  # Cambia por el nombre de tu bucket

    # Inicializa las extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)

    # Inicializa el cliente de MinIO
    minioClient = Minio(
        app.config['MINIO_ENDPOINT'],
        access_key=app.config['MINIO_ACCESS_KEY'],
        secret_key=app.config['MINIO_SECRET_KEY'],
        secure=app.config['MINIO_SECURE']
    )

    # Asegura que el bucket existe
    with app.app_context():
        if not minioClient.bucket_exists(app.config['MINIO_BUCKET']):
            minioClient.make_bucket(app.config['MINIO_BUCKET'])

    # Configurar el cargador de usuario para Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importa las rutas dentro del contexto de la aplicación
    with app.app_context():
        from . import routes
        db.create_all()  # Crea las tablas de la base de datos si no existen

    # Guarda el cliente MinIO en la aplicación para usarlo más tarde
    app.minio_client = minioClient

    return app
