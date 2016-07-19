========================
Beaker backend for redis
========================

This module created for work with `pyramid_beaker`.

.. code block: ini

    session.type = redis
    session.dsn = localhost:6379/0
    session.ttl = 86400
    session.hkey_prefix = proj-sessions
