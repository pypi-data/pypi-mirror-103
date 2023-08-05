import cryptography.exceptions
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from .rsa.exceptions import InvalidSignature
from .constants import HASH_SHA256

from .rsa.types import RSAPrivateKeySet
from .rsa.low_level import sign, verify
from .rsa.key_helpers import to_public_key_set


class MessageAuthenticator(object):
	"""Unified interface for message authentication codes."""

	def __init__(self):
		self.hash = None
		self._finalized = False
		self._verified = False

	@property
	def finalized(self) -> bool:
		return self._finalized

	@property
	def verified(self) -> bool:
		return self._verified

	@property
	def length(self):
		"""Return the number of bytes the final mac will be."""
		raise NotImplementedError

	def update(self, data: bytes) -> None:
		"""Update the hash with new data."""
		self.hash.update(data)

	def finalize(self) -> bytes:
		"""Complete the hash and sign it."""
		raise NotImplementedError

	def verify(self, signature: bytes) -> bytes:
		raise NotImplementedError


class MessageAuthenticatorRSA(MessageAuthenticator):
	"""RSA authentication implementation."""

	def __init__(self, private_key: RSAPrivateKeySet, hash_type=HASH_SHA256):
		super(MessageAuthenticatorRSA, self).__init__()
		self.private_key = private_key

		if hash_type == HASH_SHA256:
			self.hash = hashes.Hash(hashes.SHA256())
		else:
			raise RuntimeError('Hash type not supported.')

	@property
	def length(self):
		if not isinstance(self.private_key, (RSAPrivateKey, RSAPublicKey)):
			return int(self.private_key[0].key_size / 8)
		return int(self.private_key.key_size / 8)

	def finalize(self):
		if self._finalized:
			return
		self._finalized = True
		signature_hash = self.hash.finalize()
		return sign(signature_hash, self.private_key)

	def verify(self, signature):
		if self._verified:
			raise RuntimeError('Can only verify once. If you just need to check the result use the verified property')

		signature_hash = self.hash.finalize()
		verify(signature_hash, signature, to_public_key_set(self.private_key))
		self._verified = True
		return self._verified


class MessageAuthenticatorHMAC(MessageAuthenticator):
	"""HMAC-SHA256 implementation."""

	def __init__(self, private_key, hash_type=HASH_SHA256):
		super(MessageAuthenticatorHMAC, self).__init__()

		if not isinstance(private_key, (tuple, list)):
			private_key = [private_key, ]
		self.private_key = private_key

		self.hashes = list()
		if hash_type == HASH_SHA256:
			for key in private_key:
				self.hashes.append(hmac.HMAC(key, hashes.SHA256()))
		else:
			raise RuntimeError('Hash type not supported.')

	@property
	def length(self):
		return 32

	def update(self, data: bytes) -> None:
		"""Update the hash with new data."""
		for h in self.hashes:
			h.update(data)

	def finalize(self):
		if self._finalized:
			return
		self._finalized = True

		results = list()
		for h in self.hashes:
			results.append(h.finalize())
		return results[0]

	def verify(self, signature):
		if self._verified:
			raise RuntimeError('Can only verify once. If you just need to check the result use the verified property')

		for h in self.hashes:
			try:
				h.verify(signature)
				self._verified = True
				return self._verified
			except cryptography.exceptions.InvalidSignature:
				continue
		raise InvalidSignature('Signature did not match digest.')
