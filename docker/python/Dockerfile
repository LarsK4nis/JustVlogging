# Utiliza una imagen oficial de Python como imagen base
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos y lo instala para aprovechar la caché de la capa de Docker
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . /app

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Define las variables de entorno necesarias para Flask
ENV FLASK_APP app.py
ENV FLASK_ENV development

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
