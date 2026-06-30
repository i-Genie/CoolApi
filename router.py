import inspect
from container import Container
from exceptions import HTTPException
from request import Request
from response import Response
from session_store import SessionStore


class Router:
    session_store = SessionStore()
    
    def __init__(self) -> None:
        self.routes = {}
        self.middlewares = []
        self.exception_handlers = {}

    def handle_exception(
        self,
        exception_class,
        handler
    ):
        self.exception_handlers[exception_class] = handler

    def resolve_exception(
        self, 
        exception
    ):
        for(
            exception_class, handler
        ) in self.exception_handlers.items():
            if isinstance(exception, exception_class):
                return handler

        return None
            
        

    def route(self, method, path, middleware = None):
        def wrapper(handler):
            self.routes[method.upper(), path] = {
                "handler": handler,
                "middleware": middleware or []
            }
            return handler
        return wrapper


    def resolve(self, method, path):
        for (route_method, route_pattern), route_data in self.routes.items():
            pattern_paths = route_pattern.strip("/").split("/")
            path_parts = path.strip("/").split("/")

            if route_method != method.upper():
                continue

            if len(pattern_paths) != len(path_parts):
                continue

            params = {}
            matched = True

            for pattern, actual in zip(pattern_paths, path_parts):
                if (pattern.startswith("{") and pattern.endswith("}")):
                    param_name = pattern[1: -1]
                    params[param_name] = actual
                elif pattern != actual:
                    matched = False
                    break

            if matched:
                route_data["params"] = params
                return route_data
        return None

            
        
        
            

    def build_pipeline(self, request, handler):
        wrapped = handler

        for middleware in reversed(self.middlewares):
            next_handler = wrapped

            def make_wrapper(middleware, next_handler):
                def wrapper():
                    return middleware.handle(request, next_handler)
                return wrapper

            wrapped = make_wrapper(middleware, next_handler)
            
        return wrapped


    def dispatch(
        self, 
        method, 
        path, 
        query=None,
        body=None,
        headers=None,
        cookies=None,
        session=None
    ):
        primitive_types = (
            int,
            str,
            float,
            bool
        )
        
        route = self.resolve(method, path)
        # print(route)

        if not route:
            return Response(
                body="404 Not Found",
                status=404
            )

        handler = route["handler"]
        route_middlewares = route.get("middleware", [])
        route_params = route.get("params", {})
            
        request = Request(
            method, 
            path, 
            query = query or {},
            body = body or {},
            headers=headers,
            cookies=cookies,
            session=session or None
        )

        session_id = request.cookies.get(
            "session_id"
        )

        if session_id:
            request.session = Router.session_store.get(
                session_id
            )
           
        else:
            request.session = None

        container = Container()
 
        container.bind_instance(Request, request)

        signature = inspect.signature(handler)
        dependencies = []

        for param in signature.parameters.values():
            param_name = param.name
            annotation = param.annotation
            if param.annotation is inspect._empty:
                dependencies.append(
                    route_params.get(param_name)
                )
            elif annotation in primitive_types:
                raw_value = route_params.get(
                    param_name
                )

                try:
                    value = annotation(raw_value)
                except ValueError:
                    return Response(
                        body="400 Bad Request",
                        status=400
                    )
                    
                dependencies.append(
                    value
                )
            else:
                cls = param.annotation
                dependency = container.resolve(cls)
                dependencies.append(dependency)
            
        def final_handler():
            return handler(*dependencies)

        all_middlewares = (
             self.middlewares + route_middlewares
         )
 
        original_midddlewares = self.middlewares
        self.middlewares = all_middlewares
         

        pipeline = self.build_pipeline(request, final_handler)
        self.middlewares = (
            original_midddlewares
        )

        try:
            response = pipeline()
        except HTTPException as e:
            exception_handler = (
                self.resolve_exception(e)
            )
            
            if exception_handler:
                return exception_handler(e)

            if isinstance(
                e,
                HTTPException
            ):
                return Response(
                    body=e.message,
                    status=e.status
                )
            return Response(
                body="internal Server Error",
                status=500
            )

        if not isinstance(response, Response):
            response = Response(body=response)
            return response

        return response


        

    def get(self, path, middleware=None):
        return self.route(
            "GET",
            path,
            middleware
        )
        
    def post(self, path, middleware=None):
        return self.route(
            "POST",
            path,
            middleware
        )
        
    def put(self, path, middleware=None):
        return self.route(
            "PUT",
            path,
            middleware
        )
        
    def delete(self, path, middleware=None):
        return self.route(
            "DELETE",
            path,
            middleware
        )

        