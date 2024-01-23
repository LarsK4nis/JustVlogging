# minio_utils.py
from flask import current_app

def upload_file_to_minio(file, filename):
    minio_client = current_app.minio_client
    bucket_name = current_app.config['MINIO_BUCKET']
    
    # Sube el archivo
    result = minio_client.put_object(
        bucket_name,
        filename,
        file,
        file.content_length
    )
    
    # Devuelve la URL del archivo subido
    return f"{current_app.config['MINIO_ENDPOINT']}/{bucket_name}/{filename}"
