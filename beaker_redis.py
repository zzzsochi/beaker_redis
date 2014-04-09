""" Beaker backend for redis
"""

import pickle
import logging

from redis import Redis
from beaker.container import NamespaceManager, Container
from beaker.util import verify_directory

log = logging.getLogger(__name__)


class RedisBackend(NamespaceManager):
    """ Beaker backend for redis

    :param str hkey: name for redis hkey for store data
        (default: `sessions`)
    """
    hkey = 'sessions'

    def __init__(
            self,
            namespace,
            url,
            data_dir=None,
            lock_dir=None,
            hkey='sessions',
            **params):

        super().__init__(namespace)

        if lock_dir:
            self.lock_dir = lock_dir
        elif data_dir:
            self.lock_dir = data_dir + "/container_tcd_lock"
        else:
            self.lock_dir = None

        if self.lock_dir:
            verify_directory(self.lock_dir)

        self.hkey = hkey

        host, port_db = url.split(':', 1)
        port, db = (int(i) for i in port_db.split('/', 1))

        self.db = Redis(host=host, port=port, db=db)

        log.debug('sessions redis backend setuped: namespace={}'.format(namespace))

    def __contains__(self, key):
        return self.db.hexists(self.hkey, self.format_key(key))

    def __getitem__(self, key):
        data = self.db.hget(self.hkey, self.format_key(key))

        if data is not None:
            return pickle.loads(data)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        key = self.format_key(key)
        log.debug('session set key ({}: "{!r}")'.format(key, value))
        self.db.hset(self.hkey, key, pickle.dumps(value))

    def __delitem__(self, key):
        key = self.format_key(key)
        self.db.hdel(self.hkey, key)

    def format_key(self, key):
        return '{} {}'.format(self.namespace, key)

    def do_remove(self):
        log.debug('remove sessions')
        self.db.delete(self.hkey)

    def keys(self):
        raise self.db.hkeys(self.hkey)


class RedisContainer(Container):
    namespace_manager = RedisBackend
