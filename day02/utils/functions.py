from flask import session, redirect
from functools import wraps


def login_required(func):
    @wraps(func)
    def is_check(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        return redirect('/user/login/')

    return is_check
