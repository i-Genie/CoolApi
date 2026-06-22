class LoggerMiddleware:
    def handle(self, request, next):
        print(f"incoming: {request.path}")
        response = next()
        print(f"outing: {request.path}")

        return response