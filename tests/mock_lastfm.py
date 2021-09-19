from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

PORT = 8252


def extract_album(query):
    parsed = parse_qs(query)
    return parsed["album"][0]


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        album = extract_album(parsed.query)
        with open(f'./test_data/{album.lower()}.json') as f:
            response_json = json.loads(f.read())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(response_json).encode())
        return


def start_server():
    server = HTTPServer(("localhost", 8252), RequestHandler)
    print("starting server on localhost:8252")
    server.serve_forever()


if __name__ == '__main__':
    start_server()
