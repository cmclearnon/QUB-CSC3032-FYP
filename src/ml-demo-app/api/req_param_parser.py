from functools import wraps
from flask_restful import reqparse

def params_parser(*arguments):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parser = reqparse.RequestParser()
            for arg in arguments:
                parser.add_argument(arg)
            kwargs.update(parser.parse_args())
            return func(*args, **kwargs)
        return wrapper
    return decorator