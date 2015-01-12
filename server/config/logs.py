import sys
import logging


_LOADED = False


def default_config():
    global _LOADED
    if _LOADED:
        return
    else:
        _LOADED = True

    _ROOT_LOGGER = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    _ROOT_LOGGER.addHandler(handler)
    _ROOT_LOGGER.setLevel(logging.DEBUG)
