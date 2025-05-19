import os

# 경로설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # app.py가 있는 backend 디렉토리 경로
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))  # 프로젝트 루트

def set_app_root_path(path_list):
    return os.path.join(ROOT_DIR, path_list)