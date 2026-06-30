# from typing import Optional

from typing import Any, Optional


class Request:
    def __init__(
        self, 
        method, 
        path, 
        query=None, 
        body=None, 
        headers=None, 
        cookies=None,
        session=None,
        user=None
    ) -> None:
        self.method = method
        self.path = path
        self.query = query or {}
        self.body = body or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.session = session
        self.user = user
    

    