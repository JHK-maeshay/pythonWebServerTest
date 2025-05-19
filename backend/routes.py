import os
from flask import Blueprint, jsonify, request, render_template, send_from_directory
from db import get_db, set_config, get_connection
from db import select_name_from_db_where_id as getid
from import_func import set_app_img_path as ip
from import_func import set_app_mod_path as mp



# API 그룹을 정의 (이름: api)
bp = Blueprint('api', __name__)

# 이미지 업로드 디렉토리 경로
os.makedirs(os.path.join('database', 'files', 'images'), exist_ok=True)

# 모델 파일 업로드 디렉토리 경로
os.makedirs(os.path.join('database', 'files', 'safetensors'), exist_ok=True)

# 이미지 저장 폴더 경로 설정
@bp.route('/images/<filename>')
def serve_image(filename):
    image_dir = os.path.join(os.getcwd(), 'database', 'files', 'images')
    return send_from_directory(image_dir, filename)



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

@bp.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    filename = request.form.get('filename')
    safetensor_id = request.form.get('safetensor_id')

    if not image or not filename or not safetensor_id:
        return jsonify({'message': '모든 값을 입력하세요.'}), 400

    rename = getid(safetensor_id)

    if rename:
        save_path = ip(f"{rename}.png")
        try:
            image.save(save_path)
            return jsonify({'message': f'이미지가 업로드되었습니다: {save_path}'}), 200

        except Exception as e:
            return jsonify({'message': f'업로드 실패: {str(e)}'}), 500
    
    else:
        return jsonify({'message': f'매치되는 파일이 없습니다: {safetensor_id}'}), 500