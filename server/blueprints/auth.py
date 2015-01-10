import flask


def new_blueprint(github, oauth_token_storage):
    blueprint = flask.Blueprint('auth', url_prefix='/auth')


    @blueprint.route('/github-authorize')
    def github_authorize():
        return github.authorize('user:email,admin:org_hook,repo')


    @blueprint.route('/github-callback')
    @github.authorized_handler
    def github_callback(oauth_token):
        next_url = flask.request.args.get('next') or flask.url_for('index')
        if oauth_token:
            oauth_token_storage.set(oauth_token)
        return flask.redirect(next_url)


    @github.access_token_getter
    def _token_getter():
        oauth_token = oauth_token_storage.get()
        if oauth_token:
            return oauth_token
        flask.redirect(flask.url_for('.github_authorize'))


    return blueprint