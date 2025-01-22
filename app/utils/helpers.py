from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in required_roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
