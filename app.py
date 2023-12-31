import json
from flask import Flask, render_template, session
from blueprint_query.routes import blueprint_query
from blueprint_auth.routes import blueprint_auth
from access import login_required

app = Flask(__name__)
with open('configs/db.json') as f:
    app.config['db_config'] = json.load(f)

with open('configs/access.json') as f:
    app.config['access_config'] = json.load(f)

app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')


@app.route('/')
@login_required
def main_menu():
    if session.get('user_group', None):
        return render_template('internal_menu.html')
    return render_template('external_menu.html')


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
