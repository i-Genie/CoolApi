class RateLimitMiddleware:
    def handle(self, request, next):
        print(f"incoming: {request.path}")
        response = next()
        print(f"outgoing: {request.path}")

        return response