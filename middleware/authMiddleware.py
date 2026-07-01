from response import Response


class AuthMiddleware:
    def handle(
        self, 
        request, 
        next
    ):
        if not request.session:
            return Response(
                body="Unauthorized",
                status=401
            )

        return next()