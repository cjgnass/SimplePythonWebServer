import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    Page = '''
        <html> 
        <body>
        <table>
        <tr> <td>Header</td> <td>Value</td> </tr>
        <tr> <td>Date & Time</td> <td>{date_time}</td> </tr>
        <tr> <td>Client Host</td> <td>{client_host}</td> </tr>
        <tr> <td>Client Port</td> <td>{client_port}</td> </tr>
        <tr> <td>Command</td> <td>{command}</td> </tr>
        <tr> <td>Path</td> <td>{path}</td> </tr>
        </table>
        </body>
        </html>
        '''

    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):
        values = {
            'date_time': datetime.datetime.now(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path,
        }
        page = self.Page.format(**values)
        return page

    def send_page(self, page):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))


if __name__ == '__main__':
    serverAddress = ('localhost', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()