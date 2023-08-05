import os
import stat
import string
from pathlib import Path
import random
from unittest import TestCase

from cryptography.exceptions import AlreadyFinalized

from cfcrypt import InvalidSignature
from cfcrypt.constants import HASH_SHA256
from cfcrypt.message_authentication import MessageAuthenticatorRSA, MessageAuthenticatorHMAC
from cfcrypt.rsa import generate_keypair

alphabet = string.ascii_letters + string.digits + ' '


def make_message(length=60):
	return ''.join(random.choice(alphabet) for _ in range(length))


def clean_dir(temp_dir):
	if temp_dir.exists():
		for filename in temp_dir.iterdir():
			os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
			filename.unlink()
		temp_dir.rmdir()


class TestMessageAuthenticatorHMAC(TestCase):

	def setUp(self):
		random.seed(0)
		temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
		clean_dir(temp_dir)
		temp_dir.mkdir(parents=True)

		self.private_key = make_message(32).encode('utf-8')

	def tearDown(self):
		clean_dir(self.temp_dir)

	def test_create(self):
		auth = MessageAuthenticatorHMAC(self.private_key)
		self.assertIsInstance(auth, MessageAuthenticatorHMAC)

		MessageAuthenticatorHMAC(self.private_key, HASH_SHA256)
		self.assertIsInstance(auth, MessageAuthenticatorHMAC)

		self.assertRaises(RuntimeError, MessageAuthenticatorHMAC, self.private_key, 'BAD HASH TYPE')

	def test_finalized(self):
		auth = MessageAuthenticatorHMAC(self.private_key)
		self.assertFalse(auth.finalized)
		auth.finalize()
		self.assertTrue(auth.finalized)

	def test_verified(self):
		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		self.assertFalse(auth.verified)
		signature = auth.finalize()

		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		auth.verify(signature)
		self.assertTrue(auth.verified)

		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'bad data')
		self.assertRaises(InvalidSignature, auth.verify, signature)
		self.assertFalse(auth.verified)

		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		auth.finalize()
		self.assertRaises(AlreadyFinalized, auth.verify, signature)

	def test_length(self):
		auth = MessageAuthenticatorHMAC(self.private_key)
		self.assertEqual(auth.length, 32)

	def test_update(self):
		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		auth.finalize()

	def test_finalize(self):
		private_key = make_message(32).encode('utf-8')
		key_set = (private_key, self.private_key)

		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		self.assertFalse(auth.verified)
		signature = auth.finalize()

		auth = MessageAuthenticatorHMAC(key_set)
		auth.update(b'data')
		auth.verify(signature)
		self.assertTrue(auth.verified)

		auth = MessageAuthenticatorHMAC(key_set)
		auth.update(b'bad data')
		self.assertRaises(InvalidSignature, auth.verify, signature)
		self.assertFalse(auth.verified)

		# Double finalize
		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		auth.finalize()
		auth.finalize()

	def test_verify(self):
		private_key = make_message(32).encode('utf-8')
		key_set = (private_key, self.private_key)

		auth = MessageAuthenticatorHMAC(self.private_key)
		auth.update(b'data')
		self.assertFalse(auth.verified)
		signature = auth.finalize()

		auth = MessageAuthenticatorHMAC(key_set)
		auth.update(b'data')
		auth.verify(signature)
		self.assertTrue(auth.verified)

		auth = MessageAuthenticatorHMAC(key_set)
		auth.update(b'bad data')
		self.assertRaises(InvalidSignature, auth.verify, signature)
		self.assertFalse(auth.verified)

		# Double verify
		auth = MessageAuthenticatorHMAC(key_set)
		auth.update(b'data')
		auth.verify(signature)
		self.assertRaises(RuntimeError, auth.verify, signature)


class TestMessageAuthenticatorRSA(TestCase):

	def setUp(self):
		random.seed(0)
		temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
		clean_dir(temp_dir)
		temp_dir.mkdir(parents=True)

		self.private_key, self.public_key = generate_keypair()

	def tearDown(self):
		clean_dir(self.temp_dir)

	def test_create(self):
		auth = MessageAuthenticatorRSA(self.private_key)
		self.assertIsInstance(auth, MessageAuthenticatorRSA)

		MessageAuthenticatorRSA(self.private_key, HASH_SHA256)
		self.assertIsInstance(auth, MessageAuthenticatorRSA)

		self.assertRaises(RuntimeError, MessageAuthenticatorRSA, self.private_key, 'BAD HASH TYPE')

	def test_finalized(self):
		auth = MessageAuthenticatorRSA(self.private_key)
		self.assertFalse(auth.finalized)
		auth.finalize()
		self.assertTrue(auth.finalized)

	def test_verified(self):
		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		self.assertFalse(auth.verified)
		signature = auth.finalize()

		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		auth.verify(signature)
		self.assertTrue(auth.verified)

		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'bad data')
		self.assertRaises(InvalidSignature, auth.verify, signature)
		self.assertFalse(auth.verified)

		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		auth.finalize()
		self.assertRaises(AlreadyFinalized, auth.verify, signature)

	def test_length(self):
		auth = MessageAuthenticatorRSA(self.private_key)
		self.assertEqual(auth.length, self.private_key.key_size / 8)

	def test_update(self):
		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		auth.finalize()

	def test_finalize(self):
		private_key, public_key = generate_keypair()
		key_set = (private_key, self.private_key)

		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		self.assertFalse(auth.verified)
		signature = auth.finalize()

		auth = MessageAuthenticatorRSA(key_set)
		auth.update(b'data')
		auth.verify(signature)
		self.assertTrue(auth.verified)

		auth = MessageAuthenticatorRSA(key_set)
		auth.update(b'bad data')
		self.assertRaises(InvalidSignature, auth.verify, signature)
		self.assertFalse(auth.verified)

		# Double finalize
		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		auth.finalize()
		auth.finalize()

	def test_verify(self):
		private_key, public_key = generate_keypair()
		key_set = (private_key, self.private_key)

		auth = MessageAuthenticatorRSA(self.private_key)
		auth.update(b'data')
		self.assertFalse(auth.verified)
		signature = auth.finalize()

		auth = MessageAuthenticatorRSA(key_set)
		auth.update(b'data')
		auth.verify(signature)
		self.assertTrue(auth.verified)

		auth = MessageAuthenticatorRSA(key_set)
		auth.update(b'bad data')
		self.assertRaises(InvalidSignature, auth.verify, signature)
		self.assertFalse(auth.verified)

		# Double verify
		auth = MessageAuthenticatorRSA(key_set)
		auth.update(b'data')
		auth.verify(signature)
		self.assertRaises(RuntimeError, auth.verify, signature)
