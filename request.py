class Request:
    def __init__(self, method, path, user = None) -> None:
        self.method = method
        self.path = path
        self.user = user
    

    