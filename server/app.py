import flask
import flask.ext.sqlalchemy
import flask.ext.script

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
db = flask.ext.sqlalchemy.SQLAlchemy(_flask)
script_manager = flask.ext.script.Manager(_flask)

# IMPORTING DOMAIN MODULES


# SETTING THE APPLICATION UP
# Create database tables
db.create_all()

# Define the main route (the web client)
@_flask.route('/')
def root():
	return _flask.send_static_file('index.html')
	#return flask.render_template('index.html')
