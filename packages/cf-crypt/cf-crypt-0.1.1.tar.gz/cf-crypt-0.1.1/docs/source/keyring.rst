.. _keyring:

KeyRing
=======

.. py:currentmodule:: cfcrypt.keyring


KeyRing is a place to manage your keys.

It's based on a key-value store, where the key is a string and the value is an RSA PrivateKey or PrivateKeySet.


Environmental Variables
-----------------------

.. envvar:: CRYPT_KEYRING

Location to store the KeyRing files.

.. envvar:: CRYPT_KEYRING_TOKEN

The access token to unlock the KeyRing. (This is the passphrase for the generated main.pem file)


Setup
-----

On first run your need to create the key ring.

#. Set the environmental variable :envvar:`CRYPT_KEYRING` to the location you want the :py:class:`~.KeyRing` files created in.

#. Run :py:func:`KeyRing.create_key_ring` from an interactive prompt.

#. Save the produced token and add it to the environmental variable :envvar:`CRYPT_KEYRING_TOKEN`. This token unlocks the :py:class:`~.KeyRing` automatically. Alternatively you can pass in the token when instantiating :py:class:`~.KeyRing`.

The token will only be show on screen once. It is up to you to keep the token safe.

.. note::
    Without the token it will be impossible to access the stored keys.

.. code-block:: python

	>>> from cfcrypt.keyring import KeyRing
	>>> KeyRing.create_key_ring()
	Creating new KeyRing
	Creating new master key.
	KeyRing has been created in <directory>
	Your access token is:
	<random_access_token>
	The token goes into the environmental variable CRYPT_KEYRING_TOKEN
	Keep a backup of the token in a safe place as KeyRing does not keep a copy of it.


Files
-----

All the data contained in the KeyRing is stored on disk in the location specified by :envvar:`CRYPT_KEYRING`.

::

    config
      └── keyring
        ├── keyring.crpt
        └── main.pem

In the above example file structure the :envvar:`CRYPT_KEYRING` is set to '/config/keyring'

The ``keyring.crpt`` file is the serialized and encrypted KeyRing. While ``main.pem`` is the RSA key that encrypts the KeyRing on disk.
If either of these files are lost or damaged consider the KeyRing lost or damaged.

.. note::
    It is a very good idea to have a backup of these files. Without them it will be impossible to access the stored keys.



Creating a key
--------------

Creating a new key is as easy as calling :py:func:`KeyRing.create_key` with the name for the new key.

.. code-block:: python

	keyring = KeyRing()
	keyring.create_key('my_first_key')

Retrieve a key
--------------

To get a key use :py:func:`KeyRing.get_key` or :py:func:`KeyRing.get_keys` with the name of the key.
:py:func:`KeyRing.get_key` returns just the most recent key. It is the key that should be used for encrypting new data.
:py:func:`KeyRing.get_keys` returns the whole key set. This is the active encrypting key, plus previous keys. The
previous keys are for decrypting data that is older than the active key.

.. code-block:: python

	keyring = KeyRing()
	active_key = keyring.get_key('my_first_key')
	all_keys = keyring.get_keys('my_first_key')

Roll a Key
----------

Replace the existing key with a new one of the same strength. The old keys will still be available in the key set for decrypting, but all future encrypting should be done with the new key.

.. code-block:: python

	keyring = KeyRing()
	keyring.roll_key('my_first_key')


Delete a key
------------

To deleting a key use :py:func:`KeyRing.delete_key` with the name of the key.

.. warning::
    The key will be destroyed immediately. **Use with caution**.

.. code-block:: python

	keyring = KeyRing()
	keyring.delete_key('my_first_key')

Attach an Existing Key
----------------------

You can attach an existing RSA keys generated outside of KeyRing. :py:func:`KeyRing.attach_key_file` will load a PEM
encoded file from disk and attach it. While :py:func:`KeyRing.attach_key` can be used to attach and :py:class:`~cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey`

.. code-block:: python

	keyring = KeyRing()
	private_key = my_custom_key_loader()
	keyring.attach_key('my_first_key', private_key)


.. code-block:: python

	keyring = KeyRing()
	private_key = my_custom_key_loader()
	keyring.attach_key_file('my_first_key', Path('./encryption_key.pem'), 'my_pass_phrase')


Classes
----------------------

.. autoclass:: cfcrypt.keyring.KeyRing
   :members:
   :inherited-members:
   :member-order: bysource
