from flask import Blueprint, jsonify
from db import get_db

# API 그룹을 정의 (이름: api)
bp = Blueprint('api', __name__)

@bp.route('/test', methods=['GET'])
def ping():
    return jsonify({'message': 'success'})

@bp.route('/data', methods=['GET'])
def get_all_data():
    db = get_db()
    cursor = db.cursor()  # 결과를 dict로 받기 위함
    cursor.execute("SELECT * FROM safetensors") 
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results)