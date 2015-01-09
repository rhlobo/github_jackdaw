import re
import json

import flask
import flask.ext.github
import flask.ext.script
import flask.ext.session

import config.env as env


# INITIALIZING FLASK
flask_instance = _flask = flask.Flask(
	__name__,
	static_folder=env.settings('FLASK_STATIC_FOLDER'),
	template_folder=env.settings('FLASK_TEMPLATE_FOLDER'),
	static_url_path=''
)
flask_instance.config.from_object('server.config.flask_commons')
flask_instance.config.from_object(env.settings('FLASK_CONFIG_OBJECT'))


# INITIALIZING EXTENSIONS AND SERVICES
script_manager = flask.ext.script.Manager(_flask)
github = flask.ext.github.GitHub(_flask)
session_manager = flask.ext.session.Session(_flask)


# IMPORTING DOMAIN MODULES
# ...


# SETTING THE APPLICATION UP
# Routes
@_flask.route('/')
def index():
    oauth_token = _token_getter()
    if oauth_token:
    	return _flask.send_static_file('index.html')
	   #return flask.render_template('index.html')


@_flask.route('/login')
def login():
    return github.authorize('user:email,admin:org_hook,repo')


@_flask.route('/logout')
def logout():
    flask.session['oauth_token'] = oauth_token
    flask.redirect(flask.url_for('login'))


@_flask.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = flask.request.args.get('next') or flask.url_for('index')
    if oauth_token:
        flask.session['oauth_token'] = oauth_token
    return flask.redirect(next_url)


@github.access_token_getter
def _token_getter():
    oauth_token = flask.escape(flask.session.get('oauth_token'))
    if not oauth_token:
        flask.redirect(flask.url_for('login'))
    else:
        return oauth_token


@_flask.route('/api/status')
def repo():
    data = {}

    user = github.get('user')
    data['user'] = user['login']
    data['email'] = user['email']

    data['orgs'] = []
    for organization in github.get(_remove_host(user['organizations_url'])):
        orgdata = {
            'name': organization['login'],
            'avatar': organization['avatar_url']
        }
        orgdata['hooks'] = github.get('orgs/%s/hooks' % organization['login'], headers={'Accept': 'application/vnd.github.sersi-preview+json'})
        data['orgs'].append(orgdata)

    return json.dumps(data, indent=4)


def _remove_host(url):
    match = re.search(r'http[s]?://[^/]+/(.*)', url)
    return match.group(1)
