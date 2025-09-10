import datetime
import os

from http.server import HTTPServer, BaseHTTPRequestHandler

class case_no_file(object):
    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise Exception("File not found '{0}'".format(handler.path))

class case_existing_file(object):
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        handler.handle_file(handler.full_path)

class case_directory_index_file(object):
    def index_path(self, handler):
        return os.path.join(handler.full_path, "index.html")

    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.handle_file(self.index_path(handler))

class case_directory_no_index_file(object):
    def index_path(self, handler):
        return os.path.join(handler.full_path, "index.html")

    def test(self, handler):
        return os.path.isdir(handler.full_path) and not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.list_dir(handler.full_path)

class case_fail(object):
    def test(self, handler):
        return True
    def act(self, handler):
        raise Exception("Unknown Object '{0}'".format(handler.path))

class RequestHandler(BaseHTTPRequestHandler):
    Listing_Page = """ 
    <html> 
    <body>
    <h1>Listing Page</h1>
    <ul>{0}</ul> 
    </body>
    </html>
    """
    Error_Page = """
    <html>
    <body> 
    <h1>Error accessing {path}</h1> 
    <p>{e}</p>
    </body> 
    </html>
    """
    Cases = [case_no_file, case_existing_file, case_directory_index_file, case_directory_no_index_file, case_fail]

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + "/root" +  self.path
            for case in self.Cases:
                handler = case()
                if handler.test(self):
                    handler.act(self)
                    break

        except Exception as e:
            self.handle_error(e)

    def handle_file(self, full_path):
        try:
            with open(full_path, "rb") as f:
                content = f.read()
            self.send_content(content)
        except Exception as e:
            self.handle_error(e)

    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            print(full_path)
            bullets = [f'<li><a href={os.path.basename(full_path)}/{e}>{e}</a></li>' for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page)
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, e):
        content = self.Error_Page.format(path=self.path, e=e)
        self.send_content(content, 404)

    def send_content(self, content, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        try:
            self.wfile.write(content)
        except TypeError:
            self.wfile.write(content.encode('utf-8'))


if __name__ == '__main__':
    serverAddress = ('localhost', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()