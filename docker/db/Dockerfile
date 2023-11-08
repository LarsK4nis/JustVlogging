# Utiliza la imagen oficial de PostgreSQL como base
FROM postgres:13

# Opcional: Copia los scripts de inicialización si necesitas configurar la base de datos
COPY init.sql /docker-entrypoint-initdb.d/

# Las variables de entorno como la contraseña se deben definir en docker-compose.yml o en un archivo .env
