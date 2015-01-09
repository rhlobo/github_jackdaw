#!/usr/bin/env python


import sh
import sys
import flask.ext.script

import server.app as server
import wsgi


instance = server.flask_instance
manager = flask.ext.script.Manager(instance)


@manager.command
def run():
	wsgi.run()


@manager.command
def docker_build():
    sh.docker.build('-t', 'webapp', '.', _out=sys.stdout)


@manager.command
def docker_run(environment):
    sh.docker.run('-d',
                  '-e', 'ENVIRONMENT=%s' % environment,
                  '-p', '127.0.0.1:80:80',
                  'webapp')


if __name__ == '__main__':
	manager.run()