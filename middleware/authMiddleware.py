from response import Response


class AuthMiddleware:
    def handle(self, request, next):
        if not request.user:
            return Response(
                body="Unauthorized",
                status=401
            )

        return next()