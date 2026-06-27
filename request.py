class Request:
    def __init__(
        self, 
        method, 
        path, 
        query=None, 
        body=None, 
        headers=None, 
        cookies=None,
        user=None
    ) -> None:
        self.method = method
        self.path = path
        self.query = query or {}
        self.body = body or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.user = user
    

    