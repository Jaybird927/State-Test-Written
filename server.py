from flask import Flask, request, jsonify, send_file
import json
import os
import socket
from urllib.parse import urlparse, parse_qs
import sys

app = Flask(__name__)

@app.route('/api/data', methods=['GET', 'POST', 'OPTIONS'])
def handle_data():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'GET':
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "testResults": [],
                "homeroomTeachers": ["Admin"],
                "classStudents": {},
                "studentCodes": {}
            }
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=2)
        return jsonify(data)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=2)
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
        
    server_address = ('0.0.0.0', port)  # Bind to all network interfaces
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