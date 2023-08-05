Basic Usage
===========

Keys
####

Keys are used for encrypting and decrypting data.

Generate Keys
-------------

These keys are generated securely in memory.

Like all in memory variables they will disappear when your script ends.
We really need our keys to stick around for as long as we want to decrypt our data.

.. code-block:: python

	>>> from cfcrypt.rsa.key_helpers import generate_private_key
	>>> encryption_key = generate_private_key()
	>>> identity_key = generate_private_key()


Save Keys
---------

Keys can be serialized to the PEM format and saved to disk.

.. code-block:: python

	>>> from cfcrypt.rsa.key_helpers import private_key_to_pem_file
	>>> private_key_to_pem_file('./my_encryption_key.pem', encryption_key)
	>>> private_key_to_pem_file('./my_identity_key.pem', identity_key)


These `PEM` files are quite literally the keys to your data.

It's a good idea to set a strong passphrase when when serializing them. Exactly what counts as a strong
strong passphrase is a deep topic worth looking into. But 20 characters with digits, symbols, upper, and lower case is
an okay starting point.

You should also look to set the file permissions to be restrictive as possible. Readable only by the user who needs to
access the keys. A permission of `0600` is commonly used.

.. tabs::

    .. group-tab:: Linux

        .. code-block:: console

            $ chmod 600 ./my_encryption_key.pem
            $ chmod 600 ./my_identity_key.pem

    .. group-tab:: Windows

        Setting file permissions is a little more involved on windows.

        `Setting NTFS Permissions`_


Load Keys
---------

If the `PEM` files have a password you will need it to deserialize the keys from disk.

.. code-block:: python

	>>> from cfcrypt.rsa.key_helpers import pem_file_to_private_key
	>>> encryption_key = pem_file_to_private_key('./my_encryption_key.pem')
	>>> identity_key = pem_file_to_private_key('./my_identity_key.pem')


Now that we have some keys and know how to save and load them we can move on to encryption. Or if you are looking for more
details dive into :ref:`RSA keys <rsakeys>`.

As the number of keys you are using goes up you will probably want to start looking into something like :ref:`KeyRing <keyring>`.

File Encryption
###############

With our keys loaded and ready to go we can do some encryption.

Encrypt
-------

Encryption is really easy, just use :py:class:`~cfcrypt.CryptFileTextIO` like a regular file interface.

.. code-block:: python

	>>> from cfcrypt import CryptFileTextIO
	>>> with CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key) as fh:
	...	    fh.write('Super secret, secret squirrel plans.')


Decrypt
-------

Decryption is also really easy, just use :py:class:`~cfcrypt.CryptFileTextIO` like a regular file interface.

.. code-block:: python

	>>> from cfcrypt import CryptFileTextIO
	>>> with CryptFileTextIO('./my_file.crpt', 'r', encryption_key, identity_key) as fh:
	... 	data = fh.read()
	>>> data
	'Super secret, secret squirrel plans.'

That should be enough to get you going. For more details on files take a look at :ref:`Crypt FileIO <cryptfileio>`.


Object Encryption
#################

We can also directly encrypt small strings and objects. Where small means that the serialized version of the string or object is
not longer that the key size. Both :py:func:`.rsa.encrypt_object` and :py:func:`.rsa.decrypt_object` work with python objects.
Any ``JSON`` serializable object can be encrypted and decrypted.

.. code-block:: python

	>>> from cfcrypt.rsa import encrypt_object, decrypt_object
	>>> encryption_key = pem_file_to_private_key('./my_encryption_key.pem')
	>>> my_object = {1: 'a', 2: 'b', 3: 'Super secret, secret squirrel plans.'}
	>>> cipher_text = encrypt_object(my_object, encryption_key)
	>>> cipher_text
	'...'
	>>> decrypt_object(cipher_text, encryption_key)
	{1: 'a', 2: 'b', 3: 'Super secret, secret squirrel plans.'}


More details on working with objects and strings are in :ref:`RSA High Level <rsahighlevel>`.




.. _`PYPI`: https://pypi.org/project/cf-crypt/

.. _`Setting NTFS Permissions`: https://www.ntfs.com/ntfs-permissions-setting.htm