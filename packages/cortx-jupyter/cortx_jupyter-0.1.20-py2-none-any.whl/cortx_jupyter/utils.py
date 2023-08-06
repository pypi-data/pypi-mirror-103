

import time

class MultiPartUploadHelper:

    def __init__(self, seconds):
        self._seconds = seconds
        self._store = {}

    def _remove_old_keys(self, now):
        self._store = {
            key: (expires, value)
            for key, (expires, value) in self._store.items()
            if expires > now
        }

    def __getitem__(self, key):
        now = int(time.time())
        self._remove_old_keys(now)
        return self._store[key][1]

    def __setitem__(self, key, value):
        now = int(time.time())
        self._remove_old_keys(now)
        self._store[key] = (now + self._seconds, value)

    def __delitem__(self, key):
        now = int(time.time())
        self._remove_old_keys(now)
        del self._store[key]


def _get_key(config, path):
    return config.prefix + path.lstrip('/')


def _get_path(config, key):
    return '/' + key[len(config.prefix):]

def _get_full_path(key_or_path):
    return key_or_path.split('/')[-1]


@gen.coroutine
def _get_type(config, path):
    type = \
        'notebook' if path.endswith(NB_TYPE) else \
        'directory' if _is_root(path) or (yield _dir_exists(config, path)) else \
        'file'
    return type


def _get_format(config, type, path):
    type = \
        'json' if type == 'notebook' else \
        'json' if type == 'directory' else \
        'text' if mimetypes.guess_type(path)[0] == 'text/plain' else \
        'base64'
    return type


def _get_type_from_key(key):
    type = \
        'notebook' if key.endswith(NB_TYPE) else \
        'file'
    return type