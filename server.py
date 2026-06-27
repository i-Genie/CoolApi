from http.server import BaseHTTPRequestHandler, HTTPServer
import json
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
        headers = {}
        cookies = {}

        for key, values in self.headers.items():
            headers[key.lower()] = values

        query_params ={}

        for key, values in raw_query.items():
            if len(values) == 1:
                query_params[key] = values[0]
            else:
                query_params[key] = values

        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        # get cookies from header
        cookie_header = headers.get("cookie")

        if cookie_header:
            for item in cookie_header.split(";"):
                key, value = item.strip().split("=")
                cookies[key] = value
                

        raw_body = self.rfile.read(
            content_length
        )

        body = {}

        if raw_body:
            try:
                body = json.loads(raw_body.decode())
            except json.JSONDecodeError:
                self.send_response(400)

                self.send_header(
                    "Content-Type",
                    "application/json"
                )

                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "error": "Invalid JSON"
                    }).encode()
                )

                return

        # creating the response here and dispatching to the router class
        response = self.router.dispatch(
            method,
            path,
            query_params,
            body=body,
            headers = headers,
            cookies=cookies
        )

        body = response.send()

        self.send_response(
            response.status
        )

        for key, value in response.headers.items():
            if isinstance(value, list):
                for item in value:
                    self.send_header(
                        key,
                        item
                    )
            else:
                self.send_header(
                    key,
                    value
                )
                


        self.end_headers()

        self.wfile.write(
            body.encode()
        )

def run_server(router, host="127.0.0.1", port=8000):
    RequestHandler.router = router

    server = HTTPServer(
        (host, port),
        RequestHandler
    )

    print(f"server running on http://{host}:{port}")

    server.serve_forever()