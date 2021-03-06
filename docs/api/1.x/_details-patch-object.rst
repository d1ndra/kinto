If the object is missing (or already deleted), a |status-404| error is returned.
The consumer might decide to ignore it.

If the ``If-Match: "<timestamp>"`` request header is provided as described in
the :ref:`section about timestamps <server-timestamps>`, and if the object has
changed meanwhile, a |status-412| error is returned.

.. note::

    ``last_modified`` is updated to the current server timestamp, only if a
    field value was changed.


Attributes merge
----------------

The provided values are merged with the existing object. For example:

* ``{"a":"b"}`` + ``{"a":"c"}`` → ``{"a":"c"}``
* ``{"a":"b"}`` + ``{"b":"c"}`` → ``{"a":"b", "b":"c"}``
* ``{"a":"b"}`` + ``{"a":null}`` → ``{"a":null}`` : *attributes can't be removed with patch*
* ``{"a": {"b":"c"}}`` + ``{"a":{"d":"e"}}`` → ``{"a":{"d":"e"}}`` : *sub-objects are replaced, not merged*

`JSON merge <https://tools.ietf.org/html/rfc7396>`_
is currently supported using ``Content-Type: application/merge-patch+json``. This provides
support to merging sub-objects and removing attibutes. For example:

* ``{"a":"b"}`` + ``{"a":null}`` → ``{}`` 
* ``{"a": {"b":"c"}}`` + ``{"a":{"d":"e"}}`` → ``{"a":{"b:c", "d":"e"}}``
* ``{}`` + ``{"a":{"b":{"c":null}}}`` → ``{"a":{"b":{}}}``

.. note::

    `JSON-Patch <http://jsonpatch.com>`_ 
    is currently not supported. Any help is welcomed though!
    See https://github.com/Kinto/kinto/issues/458


Light response body
-------------------

If a ``Response-Behavior`` request header is set to ``light``,
only the fields whose value was changed are returned. If set to
``diff``, only the fields whose value became different than
the one provided are returned.

Permissions
-----------

In the JSON request payloads, at least one of ``data`` and ``permissions`` must be provided. Permissions can thus be modified independently from data.

The :ref:`current user id <api-current-userid>` **is always added** among the ``write`` principals.

See :ref:`api-permissions-payload`.

..
.. Kinto.core feature, not used in Kinto:
..
.. Read-only fields
.. ----------------

.. If a read-only field is modified, a |status-400| error is returned.
