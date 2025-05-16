import os

class Config:
    # MySQL 접속 정보
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'hkit')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'hkit')
    MYSQL_DB = os.getenv('MYSQL_DB', 'mydatabase')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

    # Flask 시크릿 키 (보안용, 필요시 변경)
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')