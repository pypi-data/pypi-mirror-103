RSA
===

.. py:currentmodule:: cfcrypt.rsa

``rsa`` provides helper functions to work with RSA key, encryption/decryption, and signing/verifying tasks.
It is backed by the `cryptography library`_. And more specifically the :py:mod:`cryptography.hazmat.primitives.asymmetric.rsa` module.


.. _rsakeys:

Keys
----

The key objects, :py:data:`~.rsa.RSAPrivateKey` and :py:data:`~.rsa.RSAPublicKey` are from the `cryptography library`_.

.. py:currentmodule:: cryptography.hazmat.primitives.asymmetric.rsa

.. note::

    Given a :py:data:`~.rsa.RSAPrivateKey` you can reconstruct the matching :py:data:`~.rsa.RSAPublicKey` using the method
    :py:meth:`.RSAPrivateKey.public_key`. Because of this most of functions in the module prefer to use private keys,
    and reconstruct the public key when needed.

.. py:currentmodule:: cfcrypt.rsa

Creating Keys
#############

Keys can be created with :py:func:`~.rsa.key_helpers.generate_private_key` or :py:func:`~.rsa.key_helpers.generate_keypair`

Serialized Keys
###############

You can load and save serialized keys in the `PEM` format with :py:func:`~.rsa.key_helpers.pem_file_to_private_key` and :py:func:`~.rsa.key_helpers.private_key_to_pem_file`


Key Sets
--------

To help with key life-time management we have the concept of KeySets.

KeySets are just a sequence of :py:data:`.rsa.RSAKey`
where the 0th item in the sequence is the active key. Any remaining keys in the list are considered inactive. They are kept
around for decryption and verification. They should not be used for encryption or signing.


:py:data:`~.rsa.RSAPrivateKeySet` is a list of :py:data:`~.rsa.RSAPrivateKey`. By convention the key at index 0 is the active
key. The active key (or it's :py:data:`~.rsa.RSAPublicKey` counterpart) is used for encryption operations. The remaining
inactive keys are only used to decrypt existing data.

:py:data:`~.rsa.RSAPublicKeySet` is a list of :py:data:`~.rsa.RSAPublicKey`. By convention the key at index 0 is the active
key. The active key (or it's :py:data:`~.rsa.RSAPublicKey` counterpart) is used for encryption operations. The remaining
inactive keys are only used to verify signatures on existing data.

Helpers
#######

There are helper functions for working with `KeySets` like :py:func:`~.rsa.key_helpers.to_public_key` and
:py:func:`~.rsa.key_helpers.to_public_key_set`. It's best to just pass around the private keys then use the helpers
to recover the public keys.

.. _rsahighlevel:

High Level
----------

Provides encryption/decryption helpers.

.. _rsahighlevelstring:

Both :py:func:`.rsa.encrypt_string` and :py:func:`.rsa.decrypt_string` work with strings. They handle encoding the string into bytes and back again.

.. code-block:: python

	>>> from cfcrypt.rsa import encrypt_string, decrypt_string
	>>> from cfcrypt.rsa.key_helpers import generate_keypair
	>>> private_key, public_key = generate_keypair()
	>>> my_string = 'Super secret, secret squirrel plans.'
	>>> cipher_text = encrypt_string(my_string, public_key)
	>>> cipher_text
	'...'
	>>> decrypt_string(cipher_text, private_key)
	'Super secret, secret squirrel plans.'

.. _rsahighlevelobject:

Both :py:func:`.rsa.encrypt_object` and :py:func:`.rsa.decrypt_object` work with python objects. Any ``JSON`` serializable object can be encrypted and decrypted.

.. code-block:: python

	>>> from cfcrypt.rsa import encrypt_object, decrypt_object
	>>> from cfcrypt.rsa.key_helpers import generate_keypair
	>>> private_key, public_key = generate_keypair()
	>>> my_object = ['Super secret, secret squirrel plans.', 'rendezvous at oak tree.']
	>>> cipher_text = encrypt_object(my_object, public_key)
	>>> cipher_text
	'...'
	>>> decrypt_object(cipher_text, private_key)
	['Super secret, secret squirrel plans.', 'rendezvous at oak tree.']


Low Level
---------

Provides lower level encryption/decryption, and signing/verifying helpers that operate only on ``bytes``.

:py:func:`.rsa.encrypt` and :py:func:`.rsa.decrypt` operate on bytes. Internally they manage the passing requirements.
They also offer flexibility in the type of key material provided.

:py:func:`.rsa.encrypt` accepts :py:data:`~.rsa.RSAPrivateKey`, :py:data:`~.rsa.RSAPublicKey`, and :py:data:`RSAKeySet`.
The actual encryption will be performed with the :py:data:`~.rsa.RSAPublicKey` provided, or a :py:data:`~.rsa.RSAPublicKey`
will be derived from the :py:data:`~.rsa.RSAPrivateKey`. If a :py:data:`RSAKeySet` is provided the first key in the set will be used.

.. code-block:: python

	>>> from cfcrypt.rsa import encrypt, decrypt
	>>> from cfcrypt.rsa.key_helpers import generate_private_key
	>>> private_key, public_key = generate_keypair()
	>>> my_bytes = b'Super secret, secret squirrel plans.'
	>>> cipher_text = encrypt(my_bytes, public_key)
	>>> cipher_text
	b'...'
	>>> decrypt(cipher_text, private_key)
	b'Super secret, secret squirrel plans.'

.. _rsalowlevelsign:

:py:func:`.rsa.sign` and :py:func:`.rsa.verify` operate on bytes. They can be used to verify the integrity and authenticity
of the data. Both methods operate on a hash of the data rather than the raw bytes.

If the verification fails then :py:exc:`~.rsa.InvalidSignature` is raised.


.. code-block:: python

	>>> from cfcrypt.rsa import sign, verify
	>>> from cfcrypt.rsa.key_helpers import generate_private_key
	>>> from cryptography.hazmat.primitives import hashes
	>>> private_key, public_key = generate_keypair()
	>>> hasher = hashes.Hash(hashes.SHA256())
	>>> my_bytes = b'Super secret, secret squirrel plans.'
	>>> hasher.update(my_bytes)
	>>> my_bytes_hash = hasher.digest()
	>>> my_bytes_signature = sign(my_bytes_hash, private_key)
	>>> my_bytes_signature
	b'...'
	>>> verify(my_bytes_hash, my_bytes_signature, public_key)

.. note::
    For simplicity's sake, the plain text was signed in this example. In reality you likely want to only sign the cipher text to
    prevent leaking information about the plain text.


Types
-----

Some type aliases have been created to make the code and documentation more readable.

.. autodata:: RSAPrivateKey

.. autodata:: RSAPublicKey

.. autodata:: RSAKey

.. autodata:: RSAPrivateKeySet
    :annotation: = TypeAlias

.. autodata:: RSAPublicKeySet
    :annotation: = TypeAlias

.. autodata:: RSAKeySet


API
---

Key Helpers
###########

.. automodule:: cfcrypt.rsa.key_helpers
    :members:
    :member-order: bysource

Encryption Helpers
##################

.. automodule:: cfcrypt.rsa
    :members:
    :member-order: bysource


.. _`cryptography library`: https://cryptography.io/en/latest/