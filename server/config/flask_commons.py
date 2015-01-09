import os
import random
import string


def _random_string(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# FLASK
SECRET_KEY = _random_string(18)

# FLASK-SESSION
PERMANENT_SESSION_LIFETIME = 600
SESSION_TYPE = 'filesystem'

# GITHUB-FLASK
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '8aa7177a4be39a044892')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '32e909d669015e25dd772f042f7fb6c7f5083104')
