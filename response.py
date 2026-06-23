import json


class Response:
    def __init__(self, body={}, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def send(self):
        if isinstance(self.body, dict):
            self.headers["content-Type"] = "application/json"

            return json.dumps(
                self.body
            )

        return str(self.body) 
        