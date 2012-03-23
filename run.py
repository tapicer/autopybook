from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        initial_text = self.read_file('data')
        content = self.read_file('index.html')
        content = content.replace('{{initial_text}}', self.html_escape(initial_text))
        self.wfile.write(content)
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        data = self.rfile.read(int(self.headers.getheader('content-length')))
        self.write_file('data', data)
    
    def read_file(self, path):
        return open(path, 'r').read()
    
    def write_file(self, path, content):
        open(path, 'w').write(content)
    
    html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
        }
    
    def html_escape(self, text):
        return "".join(self.html_escape_table.get(c,c) for c in text)

try:
    server = HTTPServer(('', 42842), ServerHandler)
    print 'started httpserver...'
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down server'
    server.socket.close()