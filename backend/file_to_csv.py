import csv
import os

def file_to_csv(file_info: dict, csv_path='database/data.csv'):
    headers = ['file_name', 'file_type', 'volume', 'descr', 'file_path', 'file_image_path']
    file_exists = os.path.isfile(csv_path)
    write_header = not file_exists or os.path.getsize(csv_path) == 0

    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if write_header:
            writer.writeheader()
        writer.writerow(file_info)