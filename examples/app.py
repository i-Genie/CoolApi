from exceptions import HTTPException
from middleware.authMiddleware import AuthMiddleware
from middleware.rateLimitMiddleware import RateLimitMiddleware
from request import Request
from router import Router
# from session_store import SessionStore
from userService import UserService
from response import Response
from server import run_server

router = Router()
# session_store = SessionStore()

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
        "auth": request.headers.get(
            "authorization"
        ),
        "users": [
            "John",
            "Mary"
        ],
        
        "query": [
           {
               "page": request.query.get('page'),
               "tags": request.query.get('tags'),
           }
        ]
    }

@router.post("/members")
def create_members(request: Request):
    return {
        "received": request.body
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
    # 
    
@router.get("/users/{id}")
def get_users(request: Request, id):
    return Response(
        body=id,
        status=200
    )

@router.get("/admin", middleware = [AuthMiddleware()])
def admin(request):
    return Response(
        body="403 Forbidden",
        status=403
    )

@router.get("/html")
def html(request: Request):
    return Response(
        body=f"<h1>Hello {request.path}</h1>",
        headers={
            "Content-Type": "text/html"
        }
    )

@router.get("/login")
def login(request):
    session_id = Router.session_store.create()

    Router.session_store.set(
        session_id,
        "user_id",
        42
    )
    
    response = Response(
        body = "logged in"
    )

    response.set_cookie(
        "session_id",
        session_id
    )

    return response

@router.get(
    "/profile",
    middleware=[
        AuthMiddleware()
    ]
)
def profile(request: Request):
    return {
        "user_id": request.session.get(
            "user_id"
        )
    }

@router.get(
    "logout",
    middleware=[
        AuthMiddleware()
    ]
)
def logout(request: Request):
    session_id = request.cookies.get(
        "session_id"
    )

    print(
        Router.session_store.sessions
    )

    Router.session_store.destroy(
        session_id
    )

    print(
        Router.session_store.sessions
    )

    response = Response(
        body="Logged Out"
    )

    response.delete_cookie(
       "session_id"
    )

    return response
        


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


