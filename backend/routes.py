from flask import Blueprint, jsonify, request, render_template
from db import get_db, set_config, get_connection

# API 그룹을 정의 (이름: api)
bp = Blueprint('api', __name__)

@bp.route('/test', methods=['GET'])
def ping():
    return jsonify({'message': 'success'})

@bp.route('/api/db-config', methods=['POST'])
def update_db_config():
    data = request.json
    host = data.get('host', 'localhost')
    user = data.get('user', 'hkit')
    password = data.get('password', 'hkit')
    database = data.get('database', 'mydatabase')
    port = int(data.get('port', 3306))

    try:
        # DB 설정 변경
        set_config(host, user, password, database, port)

        # 실제 연결 시도해서 문제 있으면 예외 발생
        conn = get_connection()
        conn.close()

        return jsonify({"message": "DB 설정이 업데이트되었습니다."}), 200

    except Exception as e:
        return jsonify({"message": f"DB 연결 실패: {str(e)}"}), 500

@bp.route('/data_get', methods=['GET'])
def get_all_data():
    db = get_db()
    cursor = db.cursor()  # 결과를 dict로 받기 위함
    cursor.execute("SELECT * FROM safetensors") 
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results)

@bp.route('/data_view')
def view_page():
    return render_template('data_view.html')