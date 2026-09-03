import os
from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'db'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'root_password'),
        database=os.getenv('DB_NAME', 'app_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return jsonify({"message": "API Flask funcionando correctamente"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/api/v1/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION() AS version;")
            result = cursor.fetchone()
            return jsonify({"status": "success", "db_version": result['version']}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

# Nota: Removimos app.run() porque Gunicorn gestiona el servidor en producción 
# y evitas la advertencia B104 de Bandit en GitHub Actions.