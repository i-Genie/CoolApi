import inspect

from container import Container
from request import Request


class Router:
    def __init__(self) -> None:
        self.routes = {}
        self.middlewares = []

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


    def dispatch(self, method, path):
        primitive_types = (
            int,
            str,
            float,
            bool
        )
        
        route = self.resolve(method, path)
        # print(route)

        if not route:
            return "404 Not Found"

        handler = route["handler"]
        route_middlewares = route.get("middleware", [])
        route_params = route.get("params", {})
            
        request = Request(method, path)

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
                    return "400 Bad Request"
                    
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
         

        response = pipeline = self.build_pipeline(request, final_handler)
        self.middlewares = (
            original_midddlewares
        )

        return response()


        

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

        