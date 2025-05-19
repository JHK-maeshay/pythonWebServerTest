from flask import Flask, render_template, send_from_directory, jsonify
from db import get_db, close_db
from routes import bp
import json

app = Flask(__name__)
app.config.from_object('config.Config')
app.register_blueprint(bp)

# 요청 끝날 때마다 DB 연결 종료
@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)