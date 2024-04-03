from flask import request, session, redirect, url_for
from functools import wraps

def SessionManagement(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('UserID')
        
            if not user_id:
                return redirect(url_for('Login.Sessioned'))

            user_role = session.get('Role')
            
            user_role = user_role.lower()
            roles = role.lower()

            if user_role not in roles.split(','):
                return redirect(url_for('Login.Forbidden'))

            return func(*args, **kwargs)

        return wrapper
    return decorator


def GetUserSessionDetails():
    user_role = session.get('Role')
    user_id = session.get('UserID')
    user_name = session.get('UserName')
    return (user_id,user_name,user_role)


