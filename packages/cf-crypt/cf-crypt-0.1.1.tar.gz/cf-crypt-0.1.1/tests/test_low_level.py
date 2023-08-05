import hashlib
import sys
from unittest import TestCase

from pathlib import Path
if sys.version_info[:2] <= (3, 7):
	from pathlib3x import Path

from cryptography.hazmat.primitives import hashes

from cfcrypt import DecryptionFailed, EncryptionFailed, InvalidSignature
from cfcrypt.rsa import generate_keypair, encrypt, to_public_key_set, decrypt, sign, verify


class Test(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.private_key, cls.public_key = generate_keypair()
		cls.filename = Path('./test.kenc')

	def tearDown(self):
		self.filename.unlink(missing_ok=True)

	def test_encrypt(self):
		message = 'A short message'

		# Argument combinations.
		encrypt(message.encode('utf-8'), self.public_key)
		encrypt(message.encode('utf-8'), self.private_key)

		private_key, public_key = generate_keypair()

		private_key_set = (self.private_key, private_key)
		encrypt(message.encode('utf-8'), private_key_set)

		public_key_set = to_public_key_set(private_key_set)
		encrypt(message.encode('utf-8'), public_key_set)

		# Bad arguments
		self.assertRaises(TypeError, encrypt, message.encode('utf-8'))
		self.assertRaises(AttributeError, encrypt, message.encode('utf-8'), (None,))

		# Message too long
		message = 'A short message' * 999
		self.assertRaises(EncryptionFailed, encrypt, message.encode('utf-8'), self.private_key)

	def test_round_trip(self):
		message = 'A short message'
		cypher_text = encrypt(message.encode('utf-8'), self.public_key)
		decrypted_text = decrypt(cypher_text, self.private_key).decode('utf-8')
		self.assertEqual(message, decrypted_text)

		# Wrong key type
		self.assertRaises(AttributeError, decrypt, cypher_text, self.public_key)

		# Wrong key
		wrong_private_key, wrong_public_key = generate_keypair()
		self.assertRaises(DecryptionFailed, decrypt, cypher_text, wrong_private_key)

		# Key set with right key
		private_key_set = (wrong_private_key, self.private_key)
		decrypted_text = decrypt(cypher_text, private_key_set).decode('utf-8')
		self.assertEqual(message, decrypted_text)

		# Key set with only wrong keys
		another_wrong_private_key, another_wrong_public_key = generate_keypair()
		private_key_set = (wrong_private_key, another_wrong_private_key)
		self.assertRaises(DecryptionFailed, decrypt, cypher_text, private_key_set)

	def test_sign(self):
		message = 'A short message'
		h = hashlib.sha256()
		h.update(message.encode('utf-8'))
		message_hash = h.digest()

		sign(message_hash, self.private_key)

		# ValueError: The provided data must be the same length as the hash algorithm's digest size.
		self.assertRaises(ValueError, sign, 'bad hash', self.private_key)
		# bad_hash = message_hash[:-2] + b'aa'
		# sign(bad_hash, self.private_key)

		# Wrong key type
		self.assertRaises(AttributeError, sign, message_hash, self.public_key)

		sign(message_hash, self.private_key, hashes.SHA256())

		# Bad hash type
		self.assertRaises(TypeError, sign, message_hash, self.private_key, 'sha256')
		self.assertRaises(TypeError, sign, message_hash, self.private_key, h)
		self.assertRaises(TypeError, sign, message_hash, self.private_key, hashlib.sha256)

		self.assertRaises(ValueError, sign, message_hash, self.private_key, hashes.SHA1())

		private_key, public_key = generate_keypair()
		private_key_set = (self.private_key, private_key)
		sign(message_hash, private_key_set)

	def test_verify(self):
		message = 'A short message'
		h = hashlib.sha256()
		h.update(message.encode('utf-8'))
		message_hash = h.digest()

		signature = sign(message_hash, self.private_key)
		verify(message_hash, signature, self.public_key)

		# wrong key type
		self.assertRaises(AttributeError, verify, message_hash, signature, self.private_key)

		# ValueError: The provided data must be the same length as the hash algorithm's digest size.
		self.assertRaises(ValueError, verify, 'bad hash', signature, self.public_key)

		# Detect tampering
		bad_hash = message_hash[:-2] + b'aa'
		self.assertRaises(InvalidSignature, verify, bad_hash, signature, self.public_key)

		# Key sets
		private_key, public_key = generate_keypair()
		private_key_set = (self.private_key, private_key)
		public_key_set = to_public_key_set(private_key_set)
		verify(message_hash, signature, public_key_set)

		private_key_set = (private_key, self.private_key)
		public_key_set = to_public_key_set(private_key_set)
		verify(message_hash, signature, public_key_set)
