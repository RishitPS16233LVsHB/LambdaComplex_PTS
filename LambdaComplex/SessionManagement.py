from flask import request, session, redirect, url_for
from functools import wraps

def SessionManagement(role='User'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('UserID')
        
            if not user_id:
                return redirect(url_for('Login.Sessioned'))

            user_role = session.get('Role')
            if user_role not in role.split(','):
                return redirect(url_for('Login.Forbidden'))

            return func(*args, **kwargs)

        return wrapper
    return decorator
