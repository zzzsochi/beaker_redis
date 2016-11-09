""" Beaker backend for redis.
"""
import logging
from pickle import dumps as pickle_dumps
from pickle import loads as pickle_loads

from redis import Redis
from beaker.container import NamespaceManager, Container
from beaker.util import verify_directory

log = logging.getLogger(__name__)

DEFAULT_TTL = 30 * 24 * 60 * 60  # 30 days


class RedisBackend(NamespaceManager):
    """ Beaker backend for redis.

    :param str dsn: [password@]host:port/db
        (default: `localhost:6379/0`)
    :param str hkey_prefix: name for redis hkey for store data
        (default: `session`)
    :param int ttl: ttl from last access
        (default: `2592000` (30 days))
    """
    def __init__(
            self,
            namespace,
            dsn='localhost:6379/0',
            data_dir=None,
            lock_dir=None,
            hkey_prefix='session',
            ttl=DEFAULT_TTL,
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

        host, port, db_num, password = self._parse_dsn(dsn)
        self.db = Redis(host=host, port=port, db=db_num, password=password)

        self.hkey = hkey = ':'.join((hkey_prefix, self.namespace))
        self.ttl = int(ttl)

        log.debug("session setuped: %s", hkey)

    def _parse_dsn(self, dsn):
        parts = dsn.split('@', 1)
        if len(parts) > 1:
            password, hostport = parts
        else:
            hostport = parts[0]
            password = None
        host, port_db = hostport.split(':', 1)
        port, db_num = (int(i) for i in port_db.split('/', 1))
        return host, port, db_num, password

    def __contains__(self, key):
        return self.db.hexists(self.hkey, key)

    def __getitem__(self, key):
        data = self.db.hget(self.hkey, key)

        if data is not None:
            self.db.expire(self.hkey, self.ttl)
            return pickle_loads(data)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        log.debug("session set key: %s %s %r", self.hkey, key, value)
        self.db.hset(self.hkey, key, pickle_dumps(value))
        self.db.expire(self.hkey, self.ttl)

    def __delitem__(self, key):
        log.debug("session del key: %s %s", self.hkey, key)
        self.db.hdel(self.hkey, key)
        self.db.expire(self.hkey, self.ttl)

    def do_remove(self):
        log.debug("session remove: %s", self.hkey)
        self.db.delete(self.hkey)

    def keys(self):
        keys = self.db.hkeys(self.hkey)
        self.db.expire(self.hkey, self.ttl)
        return keys


class RedisContainer(Container):
    namespace_manager = RedisBackend
