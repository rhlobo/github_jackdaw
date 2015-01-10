import re
import json
import flask


_URIPATH_REGEX = re.compile(r'http[s]?://[^/]+/(.*)')


def new_blueprint(github, basic_auth):
    blueprint = flask.Blueprint('api', url_prefix='/api/v1')


    @blueprint.route('/api/status')
    @basic_auth.required
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

        return json.dumps(data)


    def _remove_host(url):
        return _URIPATH_REGEX.search(url).group(1)


    return blueprint