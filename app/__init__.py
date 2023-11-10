from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/microblogging'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy con la configuración de la aplicación
db = SQLAlchemy(app)

# Importar las rutas después de crear la instancia de Flask
from . import routes
