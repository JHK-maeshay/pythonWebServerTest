import csv
import pickle
from db import get_db, close_db
from app import app  # Flask app 객체
from import_func import set_app_root_path as rp

def import_csv_to_db_R(csv_file_path):
    db = get_db()
    cursor = db.cursor()

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_name = row['file_name']
            file_type = row['file_type']
            volume = int(row['volume'])
            descr = row['descr']
            file_path = row['file_path']
            file_image_path = row['file_image_path']

            # 기존 데이터 확인
            cursor.execute("SELECT * FROM safetensors WHERE file_name = %s", (file_name,))
            existing = cursor.fetchone()

            if existing:
                # 완전히 동일하면 무시
                if (
                    existing['file_type'] == file_type and
                    existing['volume'] == volume and
                    existing['descr'] == descr and
                    existing['file_path'] == file_path and
                    existing['file_image_path'] == file_image_path
                ):
                    continue

                # 일부 다르면 → 업데이트
                cursor.execute(
                    """
                    UPDATE safetensors
                    SET file_type = %s,
                        volume = %s,
                        descr = %s,
                        file_path = %s,
                        file_image_path = %s
                    WHERE file_name = %s
                    """,
                    (file_type, volume, descr, file_path, file_image_path, file_name)
                )
            else:
                # 새 데이터 → 삽입
                cursor.execute(
                    """
                    INSERT INTO safetensors (file_name, file_type, volume, descr, file_path, file_image_path)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (file_name, file_type, volume, descr, file_path, file_image_path)
                )

    db.commit()
    cursor.close()
    close_db()
    print("CSV import complete.")

def load_config_from_file():
    with open(rp('database/db_config.json'), 'rb') as f:
        return pickle.load(f)

# Flask 앱 컨텍스트 내에서 실행
if __name__ == '__main__':
    loaded_config = load_config_from_file()

    # set_config 적용
    from db import set_config
    set_config(**loaded_config)

    with app.app_context():
        import_csv_to_db_R(rp('database/data.csv'))