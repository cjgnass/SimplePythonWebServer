from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    Page = b'''
    <html>
    <body> 
    <p>Hello, web!</p>
    </body>
    </html>
    '''
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.Page)

if __name__ == '__main__':
    serverAddress = ('localhost', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()