from flask_restx import Namespace

def create_namespace(name: str, description: str = None, url_prefix: str = None, with_auth: bool = True) -> Namespace:
    name = name.lower()
    if description is None:
        description = f"Operation related to {name.capitalize()}"
    decorators = []
    if with_auth:
        # decorators.append()
        pass
    return Namespace(name, description=description, path=url_prefix, decorators=decorators)