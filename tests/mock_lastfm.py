"""
This module contains a simple HTTP server designed to emulate
the last.fm API 'gettoptags' action. The server extracts the
album from the request query and returns the matching sample
response JSON from ./test_data
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

TEST_DATA = './test_data'
PORT = 8252


def _extract_album(path):
    """
    Helper to extract album from request path

    :param path: HTTP request path
    :type: str
    :return: value for 'album' in the request params
    :rtype: str
    """
    parsed = urlparse(path)
    query = parse_qs(parsed.query)
    try:
        return query["album"][0]
    except KeyError:
        return None


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        album = _extract_album(self.path)
        with open(f'./test_data/{album.lower()}.json') as f:
            response_json = json.loads(f.read())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(response_json).encode())
        return


def start_server():
    """
    No docstring required
    """
    server = HTTPServer(("localhost", 8252), RequestHandler)
    print("starting server on localhost:8252")
    server.serve_forever()


if __name__ == '__main__':
    start_server()
