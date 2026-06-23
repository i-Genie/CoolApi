class HTTPException(Exception):
    def __init__(self, message, status) -> None:
        self.message = message
        self.status = status