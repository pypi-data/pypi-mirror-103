"""Helpers for working with the cryptography RSA library."""

from .low_level import encrypt, decrypt, sign, verify
from .high_level import encrypt_string, decrypt_string, encrypt_object, decrypt_object
from .types import RSAPrivateKey, RSAPublicKey, RSAKey, RSAPrivateKeySet, RSAPublicKeySet, RSAKeySet
from .exceptions import RSAException, EncryptionFailed, DecryptionFailed, InvalidSignature
from .key_helpers import generate_private_key, generate_private_pem, generate_keypair, pem_to_private_key, pem_to_keypair, pem_file_to_private_key, pem_file_to_keypair, private_key_to_pem, private_key_to_pem_file, to_public_key, to_public_key_set

low_level = ['encrypt', 'decrypt', 'sign', 'verify']
high_level = ['encrypt_string', 'decrypt_string', 'encrypt_object', 'decrypt_object']
# key_helpers = ['generate_private_key', 'generate_private_pem', 'generate_keypair', 'pem_to_private_key', 'pem_to_keypair', 'pem_file_to_private_key', 'pem_file_to_keypair', 'private_key_to_pem', 'private_key_to_pem_file', 'to_public_key', 'to_public_key_set']
# types = ['RSAPrivateKey', 'RSAPublicKey', 'RSAKey', 'RSAPrivateKeySet', 'RSAPublicKeySet']
exceptions = ['RSAException', 'EncryptionFailed', 'DecryptionFailed', 'InvalidSignature']

__all__ = low_level + high_level + exceptions


KEY_SERIALIZATION_ENABLED = True
try:
    from cfjson import JsonTypeRegister
except ImportError:  # pragma: no cover
    KEY_SERIALIZATION_ENABLED = False


def rsa_private_key_decode(dct):
    """Decode json dict into class objects."""
    cls_name = dct['__json_type__']
    if cls_name in ('_RSAPrivateKey',):
        return pem_to_private_key(dct['private_key'].encode())
    raise TypeError()


def rsa_private_key_encode(obj):
    """Encode the object into a json safe dict."""
    return {
        '__json_type__': type(obj).__name__,
        'private_key': private_key_to_pem(obj).decode('utf-8')
    }


def register_serde():
    """Registers with cf-json serialization."""
    JsonTypeRegister.register('_RSAPrivateKey', rsa_private_key_encode, rsa_private_key_decode)


if KEY_SERIALIZATION_ENABLED:
    register_serde()
