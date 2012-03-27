from BaseHTTPServer import HTTPServer
from server import ServerHandler

try:
    server = HTTPServer(('', 42842), ServerHandler)
    print 'started server...'
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down server'
    server.socket.close()