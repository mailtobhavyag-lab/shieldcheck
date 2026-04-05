import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class Antigravity:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=['GET']):
        def wrapper(func):
            self.routes[path] = {'func': func, 'methods': methods}
            return func
        return wrapper

    def listen(self, port=8000):
        app = self
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self._handle_request('GET')

            def do_POST(self):
                self._handle_request('POST')

            def _handle_request(self, method):
                parsed_path = urllib.parse.urlparse(self.path).path
                route = app.routes.get(parsed_path)
                
                if route and method in route['methods']:
                    # Handle JSON body for POST
                    request_data = None
                    if method == 'POST':
                        content_type = self.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            length = int(self.headers.get('Content-Length', 0))
                            request_data = json.loads(self.rfile.read(length).decode('utf-8'))

                    # Call route function
                    response = route['func'](request_data) if request_data else route['func']()
                    
                    if isinstance(response, tuple):
                        content, status, content_type = response
                    else:
                        content, status, content_type = response, 200, 'text/html'
                    
                    self.send_response(status)
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    
                    if content_type == 'application/json':
                        self.wfile.write(json.dumps(content).encode('utf-8'))
                    else:
                        self.wfile.write(content.encode('utf-8') if isinstance(content, str) else content)
                else:
                    self.send_error(404, "Not Found")

        server = HTTPServer(('0.0.0.0', port), RequestHandler)
        print(f"🚀 Antigravity engine active at http://localhost:{port}")
        server.serve_forever()

app = Antigravity()
