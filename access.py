from functools import wraps

from flask import (
    session, render_template, current_app,
    request, redirect, url_for
)


def login_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return fun(*args, **kwargs)
        return redirect(url_for('blueprint_auth.start_auth'))

    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_app = request.endpoint.split('.')[0]
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
    return False


def group_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return fun(*args, **kwargs)
        return render_template('exceptions/internal_only.html')
    return wrapper
