import flask


def new_blueprint(github, oauth_token_storage):
    blueprint = flask.Blueprint('webhook', __name__, url_prefix='/hooks')


    @blueprint.route('/push')
    @blueprint.route('/pull-request')
    @blueprint.route('/push_and_pr')
    def push_and_pr():
        pass


    return blueprint