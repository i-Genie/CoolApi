from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import (urlparse, parse_qs)

# from router import Router

class RequestHandler(BaseHTTPRequestHandler):
    router = None

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        parsed = urlparse(self.path)
        
        path = parsed.path
        raw_query = parse_qs(parsed.query)
        method = self.command

        query_params ={}

        for key, values in raw_query.items():
            if len(values) == 1:
                query_params[key] = values[0]
            else:
                query_params[key] = values

        response = self.router.dispatch(
            method,
            path,
            query_params
        )

        self.send_response(
            response.status
        )

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            response.send().encode()
        )

def run_server(router, host="127.0.0.1", port=8000):
    RequestHandler.router = router

    server = HTTPServer(
        (host, port),
        RequestHandler
    )

    print(f"server running on http://{host}:{port}")

    server.serve_forever()