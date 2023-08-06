
from tornado.locks import Lock
import datetime
from traitlets import Unicode,Instance,TraitType,Type,default
from notebook.services.contents.manager import ContentsManager
from collections import namedtuple
from tornado import gen
from .cortx_authenticator import CortxAuthenticator
# from .utils import (MultiPartUploadHelper,_get_key,_get_path, _get_full_path,_get_type,_get_format,_get_type_from_key)
from .utils import (
    _run_sync,MultiPartUploadHelper,_check_directory_exists,_check_file_exists,_get_model,_save_model,_delete_notebook,_rename_notebook,_new_untitled_notebook,_get_new_notebook,_copy_notebook,_create_new_checkpoint,_restore_notebook_checkpoint,_list_all_checkpoints,_delete__notebook_checkpoint
    )
from .utils import *
import json 

import nbformat

Config = namedtuple('Config', [
    
 'prefix', 'region', 'bucket_name', 'host_name', 'cortx_authenticator',
    'multipart_uploads', 'endpoint_url'
])


# class Datetime(TraitType):
#     klass = datetime.datetime
#     default_value = datetime.datetime(1900, 1, 1)

class CortxJupyter(ContentsManager):

    bucket_name = Unicode(config=True)
    host_name = Unicode(config=True)
    region_name = Unicode(config=True)
    prefix = Unicode(config=True)
    endpoint_url = Unicode(config=True)

    authentication_class = Type(CortxAuthenticator, config=True)
    authentication = Instance(CortxAuthenticator)

    @default('authentication')
    def _default_authentication(self):
        return self.authentication_class(parent=self)

    checkpoints_class = None
    write_lock = Instance(Lock)

    @default('write_lock')
    def _write_lock_default(self):
        return Lock()

    multipart_uploads = Instance(MultiPartUploadHelper)

    @default('multipart_uploads')
    def _multipart_uploads_default(self):
        return MultiPartUploadHelper(60 * 60 * 1)

    def is_hidden(self, file_path):
        return False

    def dir_exists(self, file_path):

        @gen.coroutine
        def dir_exists_async():
            return (yield _check_directory_exists(self._config(), file_path))

        return _run_sync(dir_exists_async)

    def file_exists(self, file_path):

        @gen.coroutine
        def file_exists_async():
            return (yield _check_file_exists(self._config(), file_path))

        return _run_sync(file_exists_async)

    def get(self, file_path, file_content=True, file_type=None, file_format=None):

        @gen.coroutine
        def get_async():
            return (yield _get_model(self._config(), file_path, file_content, file_type, file_format))

        return _run_sync(get_async)

    @gen.coroutine
    def save(self, model, file_path):
        with (yield self.write_lock.acquire()):
            return (yield _save_model(self._config(), model, file_path))

    @gen.coroutine
    def delete(self, file_path):
        with (yield self.write_lock.acquire()):
            yield _delete_notebook(self._config(), file_path)

    @gen.coroutine
    def update(self, model, file_path):
        with (yield self.write_lock.acquire()):
            return (yield _rename_notebook(self._config(), file_path, model['path']))

    @gen.coroutine
    def new_untitled(self, file_path='', file_type='', extension=''):
        with (yield self.write_lock.acquire()):
            return (yield _new_untitled_notebook(self._config(), file_path, file_type, extension))

    @gen.coroutine
    def new(self, model, file_path):
        with (yield self.write_lock.acquire()):
            return (yield _get_new_notebook(self._config(), model, file_path))

    @gen.coroutine
    def copy(self, src_path, dest_path):
        with (yield self.write_lock.acquire()):
            return (yield _copy_notebook(self._config(), src_path, dest_path))

    @gen.coroutine
    def create_checkpoint(self, file_path):
        with (yield self.write_lock.acquire()):
            return (yield _create_new_checkpoint(self._config(), file_path))

    @gen.coroutine
    def restore_checkpoint(self, id, file_path):
        with (yield self.write_lock.acquire()):
            return (yield _restore_notebook_checkpoint(self._config(), id, file_path))

    @gen.coroutine
    def list_checkpoints(self, file_path):
        return (yield _list_all_checkpoints(self._config(), file_path))

    @gen.coroutine
    def delete_checkpoint(self, id, file_path):
        with (yield self.write_lock.acquire()):
            return (yield _delete__notebook_checkpoint(self._config(),id, file_path))

    def _config(self):

        return Config(
            region=self.region_name,
            bucket_name=self.bucket_name,
            host_name=self.host_name,
            cortx_authenticator=self.authentication.get_credentials,
            prefix=self.prefix,
            multipart_uploads=self.multipart_uploads,
            endpoint_url=self.endpoint_url
        )

