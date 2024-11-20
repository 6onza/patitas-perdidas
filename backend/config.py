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

# SECRET_KEY = ""