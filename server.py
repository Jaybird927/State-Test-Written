from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import socket
from urllib.parse import urlparse, parse_qs
import sys

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

class StateTestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Handle API requests
        if path == '/api/data':
            self._set_headers('application/json')
            try:
                with open('data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                # Create default data if file doesn't exist
                data = {
                    "testResults": [],
                    "homeroomTeachers": ["Admin"],
                    "classStudents": {},
                    "studentCodes": {}
                }
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=2)
            self.wfile.write(json.dumps(data).encode())
            return

        # Handle static files
        if path == '/':
            path = '/50-state-test.html'
        
        try:
            with open(path[1:], 'rb') as f:
                content = f.read()
                content_type = 'text/html'
                if path.endswith('.js'):
                    content_type = 'application/javascript'
                elif path.endswith('.css'):
                    content_type = 'text/css'
                self._set_headers(content_type)
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_POST(self):
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=2)
                self._set_headers('application/json')
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

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
    httpd = HTTPServer(server_address, StateTestHandler)
    local_ip = get_local_ip()
    print(f"\nServer running at:")
    print(f"Local:   http://localhost:{port}")
    print(f"Network: http://{local_ip}:{port}")
    print("\nPress Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 