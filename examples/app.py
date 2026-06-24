from exceptions import HTTPException
from middleware.authMiddleware import AuthMiddleware
from middleware.rateLimitMiddleware import RateLimitMiddleware
from request import Request
from router import Router
from userService import UserService
from response import Response
from server import run_server

router = Router()

# router.middlewares.append(
#     RateLimitMiddleware()
# )
# 
# 
# router.middlewares.append(
#     AuthMiddleware()
# )

@router.get("/home", middleware=[ RateLimitMiddleware()])
def home(request: Request, user_service: UserService):
    return [
        user_service.get_users(), 
    ]

@router.get("/users")
def users(request: Request):
    return {
        "users": [
            "John",
            "Mary"
        ]
    }

@router.post("/users")
def create_users(request: Request):
    raise HTTPException(
        "forbidden",
        403
    )

@router.put("/users/{id}")
def update_users(request: Request, id):
    return "hello"
    
@router.delete("/users/{id}")
def delete_users(request: Request):
    raise HTTPException(
        "forbiden",
        403
    )
    # return f"Deleted: {id}"

@router.get("/admin", middleware = [AuthMiddleware()])
def admin(request):
    return Response(
        body="403 Forbidden",
        status=403
    )


def http_exception_handler(exception):
    return Response(
        body={
            "error": exception.message,
        },
        status=exception.status
    )

router.handle_exception(
    HTTPException,
    http_exception_handler
)

# response = router.dispatch("put", "/users/2")

# print(response.status)
# print(response.send())

run_server(router)


