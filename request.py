class Request:
    def __init__(self, method, path, query=None, user = None) -> None:
        self.method = method
        self.path = path
        self.query = query or {}
        self.user = user
    

    