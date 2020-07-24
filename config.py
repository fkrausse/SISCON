import os 


SECRET_KEY = 'CLEARDB_DATABASE_URL'

MYSQL_HOST = "us-cdbr-east-02.cleardb.com"
MYSQL_USER = "bffef14ac89b72"
MYSQL_PASSWORD = "3f269b60"
MYSQL_DB = "heroku_c297a0dd5b30859"
MYSQL_PORT = 3306

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
