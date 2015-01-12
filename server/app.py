import sys

import flask
import flask.ext.github
import flask.ext.script
import flask.ext.session
import flask.ext.basicauth

import data
import config.env as env
import config.logs as logs

import blueprints.api as api
import blueprints.auth as auth
import blueprints.webhook as webhook


# CONFIGURING LOGGING
logs.default_config()


# INITIALIZING FLASK
flask_instance = _flask = flask.Flask(
	__name__,
	static_folder=env.settings('FLASK_STATIC_FOLDER'),
	template_folder=env.settings('FLASK_TEMPLATE_FOLDER'),
	static_url_path=''
)
flask_instance.config.from_object('server.config.flask_commons')
flask_instance.config.from_object(env.settings('FLASK_CONFIG_OBJECT'))

if not flask_instance.config['BASIC_AUTH_USERNAME'] or not flask_instance.config['BASIC_AUTH_PASSWORD']:
    print 'Setting non-empty BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD environment variables is mandatory. Exiting...'
    sys.exit()


# INITIALIZING EXTENSIONS AND SERVICES
# Extensions
basic_auth = flask.ext.basicauth.BasicAuth(_flask)
script_manager = flask.ext.script.Manager(_flask)
github = flask.ext.github.GitHub(_flask)
session_manager = flask.ext.session.Session(_flask)

# Services
oauth_token_storage = data.DoubleStorage(_flask, 'OAUTH_TOKEN')


# SETTING THE APPLICATION UP
# Main Routes
@_flask.route('/')
@basic_auth.required
def index():
    if oauth_token_storage.get():
        return _flask.send_static_file('index.html')
    return flask.redirect(flask.url_for('auth.github_authorize'))


# Blueprints
_flask.register_blueprint(api.new_blueprint(github, basic_auth))
_flask.register_blueprint(auth.new_blueprint(github, oauth_token_storage))
_flask.register_blueprint(webhook.new_blueprint(github, oauth_token_storage))
