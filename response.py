import json


class Response:
    def __init__(self, body={}, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = {
            k.lower(): v for k, v in (headers or {}).items()
        }

    def send(self):
        if isinstance(self.body, dict):
            if "content-type" not in self.headers:
                self.headers[
                    "content-Type"
                ] = "application/json"

            return json.dumps(
                self.body
            )
        if "content-type" not in self.headers:
            self.headers[
                "content-type"
            ] = "text/plain"

        return str(self.body) 

    def set_cookie(
        self,
        key,
        value
    ):
        if "set-cookie" not in self.headers:
            self.headers["set-cookie"] = []

        self.headers["set-cookie"].append(
            f"{key}={value}"
        )
        