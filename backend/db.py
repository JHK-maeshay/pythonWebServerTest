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

def select_name_from_db_where_id(safetensor_id):
    """
    주어진 safetensor_id에 해당하는 file_name(확장자 없이)을 반환.
    존재하지 않으면 None 반환.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT file_name FROM safetensors WHERE id = %s", (safetensor_id,))
        row = cursor.fetchone()
        if row and 'file_name' in row:
            return row['file_name'].split('.')[0]
        return None
    finally:
        cursor.close()
        conn.close()