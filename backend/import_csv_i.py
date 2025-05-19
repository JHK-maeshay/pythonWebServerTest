import csv
import pickle
from db import get_db, close_db
from app import app  # Flask 앱이 정의된 파일에서 app 객체 import
from import_func import set_app_root_path as rp

def import_csv_to_db(csv_file_path):
    db = get_db()
    cursor = db.cursor()

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO safetensors (file_name, file_type, volume, descr, file_path, file_image_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row['file_name'],
                    row['file_type'],
                    int(row['volume']),
                    row['descr'],
                    row['file_path'],
                    row['file_image_path']
                )
            )

    db.commit()
    cursor.close()
    close_db()
    print("CSV import complete.")

if __name__ == '__main__':
    user_input_n = input("DB 사용자명 입력 (default: hkit): ")  # 사용자 입력 받기
    user_input_p = input("DB 비밀번호 입력 (default: hkit): ")
    user_input_d = input("DB 이름 입력 (default: mydatabase): ")

    config_data = {
        'host': 'localhost',
        'user': user_input_n,
        'password': user_input_p,
        'database': user_input_d,
        'port': 3306
    }

    with open(rp('database/db_config.json'), 'wb') as f:
        pickle.dump(config_data, f)

    # set_config 적용
    from db import set_config
    set_config(**config_data)
    
    with app.app_context():
        import_csv_to_db(rp('database/data.csv'))