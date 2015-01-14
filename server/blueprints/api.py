import re
import json
import flask


_URIPATH_REGEX = re.compile(r'http[s]?://[^/]+/(.*)')


def new_blueprint(github, basic_auth):
    blueprint = flask.Blueprint('api', __name__, url_prefix='/api')


    @blueprint.route('/status')
    @basic_auth.required
    def status():
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

        return flask.Response(json.dumps(data), content_type='application/json')


    @blueprint.route('/hook/<org>', methods=['POST'])
    @basic_auth.required
    def createhook(org):
        hook_registration = {
            'name': 'web',
            'active': True,
            'events': ['push'],
            'config': {
                'url': 'https://webhooks.chaordicsystems.com/hooks/push_and_pr',
                'content_type': 'json'
            }
        }
        github.request('POST', 'orgs/%s/hooks' % org,
                       data=json.dumps(hook_registration),
                       headers={'Accept': 'application/vnd.github.sersi-preview+json',
                                'Content-Type': 'application/json'})
        return status()


    @blueprint.route('/hook/<org>', methods=['DELETE'])
    @basic_auth.required
    def deletehook(org):
        hooks = github.get('orgs/%s/hooks' % org, headers={'Accept': 'application/vnd.github.sersi-preview+json'})
        for hook in hooks:
            try:
                github.delete('orgs/%s/hooks/%s' % (org, hook['id']),
                              headers={'Accept': 'application/vnd.github.sersi-preview+json'})
            except:
                pass
        return status()


    def _remove_host(url):
        return _URIPATH_REGEX.search(url).group(1)


    return blueprint