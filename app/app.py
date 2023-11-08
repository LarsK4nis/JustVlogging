from flask import Flask

app = Flask(__name__)

# ... tus vistas, configuraciones de la aplicación, etc.

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    