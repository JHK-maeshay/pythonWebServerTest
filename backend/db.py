import pymysql
from flask import current_app, g
from config import Config

current_config = {
    'host': Config.MYSQL_HOST,
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'database': Config.MYSQL_DB,
    'port': Config.MYSQL_PORT
}

def set_config(host, user, password, database, port):
    global current_config
    current_config.update({
        'host': host,
        'user': user,
        'password': password,
        'database': database,
        'port': port
    })

def get_connection():
    return pymysql.connect(
        host=current_config['host'],
        user=current_config['user'],
        password=current_config['password'],
        db=current_config['database'],
        port=current_config['port'],
        cursorclass=pymysql.cursors.DictCursor
    )

def get_db():
    if 'db' not in g:
        g.db = get_connection()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()