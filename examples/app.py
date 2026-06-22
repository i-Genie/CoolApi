from middleware.authMiddleware import AuthMiddleware
from middleware.rateLimitMiddleware import RateLimitMiddleware
from request import Request
from router import Router
from userService import UserService

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

@router.post("/users")
def create_users(request: Request):
    return "User Created"

@router.put("/users/{id}")
def update_users(request: Request, id):
    return f"Updated: {id}"
    
@router.delete("/users/{id}")
def delete_users(request: Request, id: float):
    return f"Deleted: {id}"

@router.get("/admin", middleware = [AuthMiddleware()])
def admin(request):
    return "Admin"

print(router.dispatch("get", "/home"))