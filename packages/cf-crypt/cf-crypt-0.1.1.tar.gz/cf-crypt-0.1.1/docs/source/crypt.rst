Crypt
=====
.. currentmodule:: cfcrypt

Provides a container format and implementation to store files on disk encrypted.

.. _cryptfileio:

FileIO
------

:py:class:`~cfcrypt.CryptFileTextIO` is a `file object`_ that provides a transparent way to read and write data to a
file without worrying about the details of the encryption or verification.


.. code-block:: python

	>>> from cfcrypt import CryptFileTextIO
	>>> from cfcrypt.rsa.key_helpers import generate_private_key
	>>> encryption_key = generate_private_key()
	>>> identity_key = generate_private_key()
	>>> fh = CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key)
	>>> fh.write('Super secret, secret squirrel plans.')
	>>> fh.close()
	>>> fh = CryptFileTextIO('./my_file.crpt', 'r', encryption_key, identity_key)
	>>> fh.read()
	'Super secret, secret squirrel plans.'

:py:class:`~cfcrypt.CryptFileTextIO` provides the text interface with standard methods like :py:meth:`CryptFileTextIO.readlines` and :py:meth:`CryptFileTextIO.writelines`.


There is also a binary version, :py:class:`~cfcrypt.CryptFileBinaryIO`.


Both :py:class:`~cfcrypt.CryptFileTextIO` and :py:class:`~cfcrypt.CryptFileBinaryIO` are based on :py:class:`io.RawIOBase`
and as such can be used anywhere a normal io buffer object can be used. For example you can pass them into a csv or json
library for plug and play encryption.


Writing
#######

.. code-block:: python

	from cfcrypt import CryptFileTextIO
	from cfcrypt.rsa.key_helpers import generate_private_key

	encryption_key = generate_private_key()
	identity_key = generate_private_key()

	with CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key) as fh:
		fh.write('Super secret, secret squirrel plans.')

Reading
#######

.. code-block:: python

	from cfcrypt import CryptFileTextIO
	from cfcrypt.rsa.key_helpers import generate_private_key

	encryption_key = generate_private_key()
	identity_key = generate_private_key()

	with CryptFileTextIO('./my_file.crpt', 'r', encryption_key, identity_key) as fh:
		data = fh.read()

Appending
#########

.. code-block:: python

    from pathlib import Path
    from cfcrypt import CryptFileTextIO
    from cfcrypt.rsa.key_helpers import generate_private_key

    encryption_key = generate_private_key()
    identity_key = generate_private_key()

    input_filename = Path('./my_file.crpt')
    output_filename = input_file.with_suffix('.temp')

    input_file = CryptFileTextIO(input_filename, 'rb', encryption_key, identity_key)
    output_file = CryptFileTextIO(output_filename, 'wb', encryption_key, identity_key)

    with input_file as in_fh, output_file as out_fh:
        data = in_fh.read()
        out_fh.write(data)
        out_fh.write('Updated data.')

    output_filename.replace(input_filename)


.. _fileutils:

File Utilities
--------------

:py:mod:`~cfcrypt.file_utils` contains for helpers for working with files and folders.

For encrypting we have:

 * :py:func:`~file_utils.encrypt_folder`
 * :py:func:`~file_utils.encrypt_files`
 * :py:func:`~file_utils.encrypt_file`

And the matching decryption:
 * :py:func:`~file_utils.decrypt_folder`
 * :py:func:`~file_utils.decrypt_files`
 * :py:func:`~file_utils.decrypt_file`


There is also :py:func:`~file_utils.secure_file_move` which takes a plain text file and moves it to a new location and encrypts it.


Design
------

We use a hybrid encryption model using both `RSA` and `AES` encryption. `AES` is used to encrypt & decrypt the file payload.
While `RSA` to manage access to the `AES` keys and to provide integrity checks.

Writing
#######

#. The `RSA` encryption key, and the `RSA` identity key key are provided.
#. A random `AES` symmetric key is generated for this and only this file.
#. The file is open for writing. The file header is created with details of the encryption scheme used.
#. The `AES` symmetric key is encrypted using the `RSA` public key. This encrypted key is written to the file header.
#. Plain text data is encrypted using `AES-CTR` and the symmetric key. The encrypted data is written to the file.
#. On finalization of the file, the file is signed with the `RSA` private key. The signature is then appended to the file.

.. note::
	Data can only be written to the file sequentially. Seeking is not permitted in writing mode.
	Once closed the	file is finalized and no further writing is permitted.

Reading
#######

#. The `RSA` encryption key, and the `RSA` identity key key are provided.
#. The signature is read from the end of the file. The `RSA` identity key is used to verify the integrity of the file.
#. The `RSA` encryption key is used to decode the `AES` symmetric key.
#. On read the `AES` symmetric key is used to decrypt the payload data to plain text.


Encryption
##########

Any `RSA` keys with a bit length greater than 512 can be used.
See :ref:`RSA keys section <rsakeys>` for more details on generating and working with keys.

For the file encryption we are using the :py:class:`~cryptography.hazmat.primitives.ciphers.algorithms.AES` algorithm in
:py:class:`~cryptography.hazmat.primitives.ciphers.algorithms.CTR` mode. This is a stream cipher mode and doesn't require
padding. By itself `AES-CTR` is malleable, that is, changes in the cipher text can cause changes the plain text.
To protect against this the entire file is signed with an `RSA-SHA256` signature using the integrity key.

The :py:class:`~cryptography.hazmat.primitives.ciphers.algorithms.AES` key material and nonce are both generated using
:py:func:`os.urandom` on a per file basis and never reused for future encryption. The :py:class:`~cryptography.hazmat.primitives.ciphers.algorithms.AES`
key material is encrypted using the `RSA` encryption key and stored with the data in the file.

It is possible to use the same `RSA` key for both the encryption key and and integrity key. But this is a bad practise.
It's much better to only use a key for a single task.


Limitations
###########

This approach is only as secure as the RSA keys used to (un)lock the files. Both the pubic and private key need to be
kept secure. Anyone with the public key can generate encrypted files. Anyone with the private key can read the
encrypted files.


The interface is setup for 'write once, read many' operations.
There is no way to edit or append to the encrypted file once written. If you want to make changes to the file, read it into
plane text, make the changes, and write out a new encrypted file.


Read performance is better when reading sequentially in large chunks. Many small reads or seeking around in the file has an
overhead as the decryptor needs to be re-initialized.

Weaknesses
##########

*Issue*
	AES-CTR is a streaming cipher and as such doesn't use padding. This reveals the exact length of the plain text.

*Mitigation*
	If you are sensitive to file length you need to manage your own padding.



*Issue*
	Any reuse of the key + IV / nonce would be a significant problem.

*Mitigation*
	Each file uses a unique and random random key, iv and/or nonce.




*Issue*
	AES-CTR alone is malleable. Changes in the cipher text can make changes in the plain text.

*Mitigation*
	RSA signing detects tampering and provides authentication. Make sure you verify the file integrity before trusting the data.




*Issue*
	AES-CTR should not by used for extremely large file (2 ** 64 bytes) as the nonce can wrap around and be reused.

*Mitigation*
	Keep single file sizes low. Less than a terabyte is very safe.


Classes
-------

.. autoclass:: CryptFileTextIO
   :members:
   :inherited-members:
   :member-order: bysource


.. autoclass:: CryptFileBinaryIO
   :members:
   :inherited-members:
   :member-order: bysource


.. autoexception:: CryptException
	:members:
	:member-order: bysource


Functions
---------

.. automodule:: cfcrypt.file_utils
   :members:
   :inherited-members:
   :member-order: bysource


.. _`file object`: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files