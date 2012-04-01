from BaseHTTPServer import BaseHTTPRequestHandler

class ServerHandler(BaseHTTPRequestHandler):
    def get_id(self):
        # filter out the path used for the id
        return filter(lambda c: c.isalnum(), self.path)
    
    def do_GET(self):
        if self.path == '/favicon.ico':
            # 404 favicon.ico to avoid processing the whole page when the browser requests the favicon
            self.send_response(404)
            self.end_headers()
        elif self.path == '/jquery.filter_input.js':
            # serve the jquery lib used to filter non alphanumeric characters from the id
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            self.wfile.write(self.read_file('jquery.filter_input.js'))
        else:
            self.send_response(200)
            self.end_headers()
            id = self.get_id()

            # set initial text according to whether the id is given
            if id:
                initial_text = self.read_file(id)
            else:
                initial_text = 'To start using autopybook write some id and press the "Load" button (or hit enter).'
            
            # get the html and replace placeholders
            content = self.read_file('index.html')
            content = content.replace('{{initial_text}}', self.html_escape(initial_text)) # avoid XSS and broken HTML issues escaping the text
            content = content.replace('{{initial_id}}', id)
            content = content.replace('{{initial_expl}}', 'Write some text below and it will be auto-saved for your id.' if id else '')
            self.wfile.write(content)
    
    def do_POST(self):
        id = self.get_id()
        if id:
            # save POST body for the given id
            self.send_response(200)
            self.end_headers()
            data = self.rfile.read(int(self.headers.getheader('content-length')))
            self.write_file(id, data)
    
    def read_file(self, path):
        try:
            return open(path, 'r').read()
        except IOError:
            return ''
    
    def write_file(self, path, content):
        open(path, 'w').write(content)
    
    html_escape_table = { "&": "&amp;", '"': "&quot;", "'": "&apos;", ">": "&gt;", "<": "&lt;" }
    
    def html_escape(self, text):
        return "".join(self.html_escape_table.get(c, c) for c in text)