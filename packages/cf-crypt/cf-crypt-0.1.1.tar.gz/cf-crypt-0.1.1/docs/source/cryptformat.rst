File Format
===========
.. currentmodule:: cfcrypt.file_format

A container format and implementation to store files on disk encrypted.

The crpt file format is a binary format consisting of a small header followed by an encrypted data payload and finally an
optional signature or `MAC`.

Header
------

The header has a few different parts.

File Type
#########

The file type is a struct 5 bytes long with only two fields.

+--------------------+------------------+-------------------------------+
|        Name        |    Data Type     | Example                       |
+====================+==================+===============================+
| Magic              | 4 Char           | |magic_bytes|                 |
+--------------------+------------------+-------------------------------+
| Version            | 1 Unsigned Byte  | 001                           |
+--------------------+------------------+-------------------------------+

This is used to find the correct :py:class:`~ContainerFormat` class to parse the remainder
of the header. This split allows us to modify the file format as needed while still maintaining backwards compatibility.
Or at least that the theory.

.. |magic_bytes| replace:: :py:data:`~ContainerFormat.magic_bytes`


Fixed Size Fields
#################

First up is a block of fixed size fields. These are fields that are the same size no matter what the data is. All data is little endian.

The following six fields from :py:class:`ContainerFormatV1` are fixed size.

+--------------------+------------------+-------------------------------+
|        Name        |    Data Type     | Example                       |
+====================+==================+===============================+
| algorithm          | Unsigned Byte    | |ALGO_AES|                    |
+--------------------+------------------+-------------------------------+
| algorithm mode     | Unsigned Byte    | |ALGO_MODE_CTR|               |
+--------------------+------------------+-------------------------------+
| algorithm pad      | Unsigned Byte    | |PAD_NONE|                    |
+--------------------+------------------+-------------------------------+
| algorithm mac      | Unsigned Byte    | |MAC_RSA_SIGNED|              |
+--------------------+------------------+-------------------------------+
| algorithm mac hash | Unsigned Byte    | |HASH_SHA256|                 |
+--------------------+------------------+-------------------------------+
| chunk size         | Integer          | -1                            |
+--------------------+------------------+-------------------------------+

.. currentmodule:: cfcrypt

.. |ALGO_AES| replace:: :py:data:`constants.ALGO_AES`
.. |ALGO_MODE_CTR| replace:: :py:data:`constants.ALGO_MODE_CTR`
.. |PAD_NONE| replace:: :py:data:`constants.PAD_NONE`
.. |MAC_RSA_SIGNED| replace:: :py:data:`constants.MAC_RSA_SIGNED`
.. |HASH_SHA256| replace:: :py:data:`constants.HASH_SHA256`
.. |MAC_HMAC| replace:: :py:data:`constants.MAC_HMAC`

.. currentmodule:: cfcrypt.file_format

Variable Fields
###############

Following that are fields that point to data else where in the file. These are needed for data that could be variable length.
All of the offsets are in decimal bytes and are relative to start of the start of the file.

+--------------------+------------------+-------------------------------+
|        Name        |    Data Type     | Example                       |
+====================+==================+===============================+
| nonce offset       | Unsigned Integer | 36                            |
+--------------------+------------------+-------------------------------+
| nonce length       | Unsigned Integer | 16                            |
+--------------------+------------------+-------------------------------+
| key offset         | Unsigned Integer | 52                            |
+--------------------+------------------+-------------------------------+
| key length         | Unsigned Integer | 256                           |
+--------------------+------------------+-------------------------------+
| data offset        | Unsigned Integer | 308                           |
+--------------------+------------------+-------------------------------+
| mac length         | Half Integer     | 256                           |
+--------------------+------------------+-------------------------------+

This is the end of the fields.

Variable Size Data
##################

After the fields comes the variable sized data. This is described in the `Variable Fields`_ section. The data is just
runs together with no deliminators. You need to rely on the offset's and lengths to unpack it correctly.

The last two chucks of variable data are special. The `data offset` has no matching data length field, and the `mac length`
has no matching offset. The missing data is calculated by :py:class:`~ContainerFormat` at load time based
on the file size.

While it would be nice have this data in file, it is not necessarily known when the header is generated.
Going back to fill in the size on finalization would be possible, but would greatly complicate the hashing
process for MAC and signatures.


Version 1
---------

While there is currently only a single version of the file format. The design is in place to cater to the different data types we may need.

Version 1 is hard coded to use |ALGO_AES|, in |ALGO_MODE_CTR| mode. We don't need padding as CTR is a streaming cipher.
For MAC we are using |MAC_RSA_SIGNED| with |HASH_SHA256|.

Other permutations are possible but will need to be implemented.

Switching to |MAC_HMAC| would be straight forward, but it lacks the authentication of `RSA`. Any one with a copy of the
public encryption key would be able to encrypt files.

Switching to a block based cipher on the other hand would be more complex as we would need to manage the padding carefully.


Constant Settings
-----------------

.. currentmodule:: cfcrypt

.. automodule:: cfcrypt.constants
       :members:

.. currentmodule:: cfcrypt.file_format

Classes
-------

.. autoclass:: ContainerFormat
   :members:
   :inherited-members:
   :member-order: bysource
