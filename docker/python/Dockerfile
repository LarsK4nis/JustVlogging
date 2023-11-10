# Utiliza una imagen oficial de Python como imagen base
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar la caché de la capa de Docker
COPY requirements.txt .

# Instala los paquetes necesarios especificados en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código de aplicación al contenedor
COPY . .

# Indica el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# El comando para ejecutar la aplicación
CMD ["python3", "app.py"]