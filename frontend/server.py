from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class FrontendHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('localhost', 3000), FrontendHandler)
    print("Serving frontend on http://localhost:3000")
    server.serve_forever()
