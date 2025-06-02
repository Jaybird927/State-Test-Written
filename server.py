from flask import Flask, request, jsonify, send_file
import json
import os
import socket
from urllib.parse import urlparse, parse_qs
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB setup
try:
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    db = client['state_test_db']
    collection = db['test_data']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # Fallback to in-memory storage if MongoDB is not available
    collection = None

def get_data():
    if collection:
        data = collection.find_one({'_id': 'main'})
        if data:
            return json.loads(json_util.dumps(data))
    return {
        "testResults": [],
        "homeroomTeachers": ["Admin"],
        "classStudents": {},
        "studentCodes": {}
    }

def save_data(data):
    if collection:
        collection.update_one(
            {'_id': 'main'},
            {'$set': data},
            upsert=True
        )
    return True

@app.route('/api/data', methods=['GET', 'POST', 'OPTIONS'])
def handle_data():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'GET':
        return jsonify(get_data())
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            save_data(data)
            return jsonify({"status": "success"})
        except Exception as e:
            return str(e), 500

@app.route('/', defaults={'path': '50-state-test.html'})
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_file(path)
    except:
        return 'File not found', 404

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_local_ip():
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def run_server(port=5000):
    if is_port_in_use(port):
        print(f"Error: Port {port} is already in use. Please make sure no other server is running.")
        sys.exit(1)
        
    local_ip = get_local_ip()
    print(f"\nServer running at:")
    print(f"Local:   http://localhost:{port}")
    print(f"Network: http://{local_ip}:{port}")
    print("\nPress Ctrl+C to stop the server")
    try:
        app.run(host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == '__main__':
    run_server() 