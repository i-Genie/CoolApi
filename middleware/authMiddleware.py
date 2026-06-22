class AuthMiddleware:
    def handle(self, request, next):
        if not request.user:
            return "404 Unauthorized"

        return next()