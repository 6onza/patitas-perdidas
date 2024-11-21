import os

DEBUG = True

# Configuración de la base de datos
DB_CONFIG = {
    'MYSQL_HOST': '127.0.0.1',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': '',
    'MYSQL_DB': 'patitas_perdidas',
    'MYSQL_PORT': 3306, 
    'MYSQL_UNIX_SOCKET': '/opt/lampp/var/mysql/mysql.sock'
}

# Configuración de uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit

# Configuración de CORS
CORS_ORIGIN = [
    'http://localhost:5001', 
    'http://localhost:5000', 
    'http://127.0.0.1:5000', 
    'http://127.0.0.1:5001'
]
CORS_ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
CORS_ALLOWED_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin']

# SECRET_KEY = ""