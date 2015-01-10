import flask


def new_blueprint(github, oauth_token_storage):
    blueprint = flask.Blueprint('webhook', url_prefix='/hooks')


    return blueprint