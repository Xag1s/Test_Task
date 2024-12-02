from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from functools import wraps
from .models import User


def check_access(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if user.role not in roles:
                abort(403, description="Access denied")

            return func(*args, **kwargs)

        return wrapper

    return decorator
