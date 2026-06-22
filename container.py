import inspect


class Container:
    def __init__(self) -> None:
        self.instances = {}

    def bind_instance(self, cls, instance):
         self.instances[cls] = instance
         
    def resolve(self, cls):
        if cls in self.instances:
            return self.instances[cls]

        if cls.__init__ is object.__init__:
            return cls()

        signature = inspect.signature(cls.__init__)
        dependencies = []

        for param in signature.parameters.values():
            if param.name == "self":
                continue
            dependency_class = param.annotation
            dependency = self.resolve(dependency_class)
            dependencies.append(dependency)
        
        return cls(*dependencies)