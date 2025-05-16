import csv
from db import get_db, close_db
from app import app  # Flask 앱이 정의된 파일에서 app 객체 import

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
    with app.app_context():
        import_csv_to_db('../database/data.csv')
