from flask import current_app
from werkzeug.utils import secure_filename
from minio.error import S3Error

def upload_file_to_minio(file):
    """
    Sube un archivo al bucket de MinIO y devuelve su URL presignada para acceso.

    Args:
    - file: Objeto archivo Flask request.files['nombre_del_input']

    Returns:
    - URL presignada del archivo subido o None si hay un error.
    """
    minio_client = current_app.minio_client
    bucket_name = current_app.config['MINIO_BUCKET']

    # Genera un nombre de archivo seguro
    filename = secure_filename(file.filename)

     # Verifica si el archivo está vacío (es decir, ya se ha leído el stream)
    if file.content_length == 0:
        # Restablece el puntero al inicio del stream
        file.seek(0)
        
    # Intenta subir el archivo a MinIO
    print("Antes del try")
    try:
        minio_client.put_object(
            bucket_name,
            filename,
            file,
            length=file.content_length,
            content_type=file.content_type
        )
        print("ESTAMOS")
        print(file.content_length)
        print("Estamos 2")
        # Genera una URL presignada para el acceso al archivo
        
        url = minio_client.presigned_get_object(bucket_name, filename)
        return url
    except S3Error as e:
        current_app.logger.error(f"Error al subir archivo a MinIO: {e}")
        return None


