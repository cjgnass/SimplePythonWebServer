import datetime
import os

from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    Page = b"""
    <html>
    <body>
    <h1>Bruh</h1>
    </body>
    </html>
    """
    Error_Page = b"""
    <html>
    <body> 
    <h1>Error accessing {path}</h1> 
    <p>{e}</p>
    </body> 
    </html>
    """

    def do_GET(self):
        try:
            full_path = os.getcwd() + self.path

            if not os.path.exists(full_path):
                raise FileNotFoundError("'{0}' not found".format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise Exception("Unknown Object '{0}'".format(self.path))
        except Exception as e:
            self.handle_error(e)

    def handle_file(self, full_path):
        try:
            with open(full_path, "rb") as f:
                content = f.read()
            self.send_content(content)
        except Exception as e:
            self.handle_error(e)


    def handle_error(self, e):
        content = self.Error_Page.format(path=self.path, e=e)
        self.send_content(content, 404)

    def send_content(self, content, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    serverAddress = ('localhost', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()