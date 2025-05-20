import os
from flask import Blueprint, jsonify, request, render_template, send_from_directory
from db import get_db, set_config, get_connection
from db import select_name_from_db_where_id as getid

# API 그룹을 정의 (이름: api)
bp = Blueprint('api', __name__)

# 업로드 디렉토리 설정
os.makedirs(os.path.join('database', 'files', 'images'), exist_ok=True)
os.makedirs(os.path.join('database', 'files', 'safetensors'), exist_ok=True)

# 이미지 서빙
@bp.route('/files/images/<filename>')
def serve_image(filename):
    # 현재 파일(예: routes.py) 기준으로 이미지 디렉토리 계산
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # project-root
    image_dir = os.path.join(base_dir, 'database', 'files', 'images')           # 절대경로 생성
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
    from import_func import set_app_img_path as ip

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
    
@bp.route('/upload_safetensors', methods=['POST'])
def upload_safetensors():
    from file_to_csv import file_to_csv
    from import_csv_r import import_csv_to_db_R
    from db import get_id_by_filename
    from import_func import set_app_mod_path as mp
    from import_func import set_app_root_path as rp

    file = request.files.get('file')
    filename = request.form.get('filename')
    filedescr = request.form.get('descr')

    if not file or not filename:
        return jsonify({'message': '실제 파일이 없습니다.'}), 400

    save_path = mp(f"{filename}.safetensors")
    try:
        file.save(save_path)

        # (1) CSV 작성
        file_info = {
            'file_name': f"{filename}.safetensors",
            'file_type': 'checkpoint',
            'volume': os.path.getsize(save_path),
            'descr': filedescr,
            'file_path': f"/files/safetensors/{filename}.safetensors",
            'file_image_path': f"/files/images/{filename}.png"
        }
        file_to_csv(file_info)

        # (2) DB 삽입
        import_csv_to_db_R(rp('database/data.csv'))

        # (3) 삽입된 ID 조회
        new_id = get_id_by_filename(file_info['file_name'])

        return jsonify({
            'message': f'Safetensors 파일이 업로드되고 DB에 등록되었습니다.',
            'id': new_id
        }), 200
    except Exception as e:
        return jsonify({'message': f'업로드 실패: {str(e)}'}), 500
    
@bp.route('/search')
def search_files():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])  # 빈 검색어이면 빈 리스트 반환

    conn = get_db()
    cursor = conn.cursor()

    # 예: file_name 또는 descr 컬럼에서 검색어 포함 여부 확인
    sql = """
        SELECT id, file_name, file_type, volume, descr, file_path, file_image_path
        FROM safetensors
        WHERE file_name LIKE %s OR descr LIKE %s
    """
    like_query = f'%{query}%'
    cursor.execute(sql, (like_query, like_query))
    results = cursor.fetchall()

    cursor.close()

    print("검색 결과:", results)
    return jsonify(results)