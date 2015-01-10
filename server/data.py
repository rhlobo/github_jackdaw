import flask


class DoubleStorage(object):

    def __init__(self, app, key):
        self.config_storage = AppConfigStorage(app, key)
        self.session_storage = SessionStorage(app, key)

    def get(self):
        value = self.config_storage.get()
        if not value:
            value = self.session_storage.get()
        return value

    def set(self, value):
        self.config_storage.set(value)
        self.session_storage.set(value)


class AppConfigStorage(object):

    def __init__(self, app, config_key):
        self.flask_instance = app
        self.config_key = config_key

    def get(self):
        if self.config_key in self.flask_instance:
            return self.flask_instance[self.config_key]
        return None

    def set(self, value):
        self.flask_instance[self.config_key] = value


class SessionStorage(object):

    def __init__(self, app, session_key):
        self.flask_instance = app
        self.session_key = session_key

    def get(self):
        if self.session_key in flask.session:
            return flask.escape(flask.session.get(self.session_key))
        return None

    def set(self, value):
        flask.session[self.session_key] = value