import os
import stat
import string
import sys
from unittest import TestCase

import random

from cfcrypt.rsa import generate_keypair, encrypt_string, decrypt_string, encrypt_object, decrypt_object
from cfcrypt.rsa.exceptions import MessageTooLongForKey, DecryptionFailed

from pathlib import Path
if sys.version_info[:2] <= (3, 7):
	from pathlib3x import Path

alphabet = string.ascii_letters + string.digits + ' '


def make_message(length=60):
	return ''.join(random.choice(alphabet) for _ in range(length))


def clean_dir(temp_dir):
	if temp_dir.exists():
		for filename in temp_dir.iterdir():
			os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
			filename.unlink()
		temp_dir.rmdir()


class Test(TestCase):

	def setUp(self):
		random.seed(0)
		temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
		clean_dir(temp_dir)
		temp_dir.mkdir(parents=True)

		self.private_key, self.public_key = generate_keypair()

	def tearDown(self):
		clean_dir(self.temp_dir)

	def test_encrypt_string(self):
		msg = make_message(60)
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)

	def test_encrypt_string_too_long(self):
		msg = make_message(190)
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)

		msg = make_message(191)
		self.assertRaises(MessageTooLongForKey, encrypt_string, msg, self.public_key)

	def test_encrypt_string_unicode(self):
		msg = '🎈🎈🎈🎈🎈'
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)

	def test_encrypt_key_types(self):
		msg = make_message(60)
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)

		msg = make_message(60)
		cypher = encrypt_string(msg, self.private_key)
		self.assertNotEqual(msg, cypher)

		private_key_2, public_key_2 = generate_keypair()

		msg = make_message(60)
		cypher = encrypt_string(msg, (public_key_2, self.public_key))
		self.assertNotEqual(msg, cypher)

		msg = make_message(60)
		cypher = encrypt_string(msg, (self.private_key, private_key_2))
		self.assertNotEqual(msg, cypher)

	def test_decrypt_string(self):
		msg = make_message(60)
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		msg = '🎈🎈🎈🎈🎈'
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		msg = make_message(60)
		cypher = encrypt_string(msg, self.private_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		msg = make_message(60)
		cypher = encrypt_string(msg, self.private_key)
		self.assertNotEqual(msg, cypher)
		# AttributeError: '_RSAPublicKey' object has no attribute 'decrypt'
		self.assertRaises(AttributeError, decrypt_string, cypher, self.public_key)

	def test_decrypt_key_types(self):
		msg = make_message(60)
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		msg = make_message(60)
		cypher = encrypt_string(msg, self.private_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		private_key_2, public_key_2 = generate_keypair()

		msg = make_message(60)
		cypher = encrypt_string(msg, (public_key_2, self.public_key))
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, private_key_2)
		self.assertEqual(msg, result)
		# Was encrypted with newer key
		self.assertRaises(DecryptionFailed, decrypt_string, cypher, self.private_key)
		# Try key set
		result = decrypt_string(cypher, (self.private_key, private_key_2))
		self.assertEqual(msg, result)

		msg = make_message(60)
		cypher = encrypt_string(msg, (private_key_2, self.private_key))
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, private_key_2)
		self.assertEqual(msg, result)
		# Was encrypted with newer key
		self.assertRaises(DecryptionFailed, decrypt_string, cypher, self.private_key)
		# Try key set
		result = decrypt_string(cypher, (self.private_key, private_key_2))
		self.assertEqual(msg, result)


class TestObjects(TestCase):

	def setUp(self):
		random.seed(0)
		temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
		clean_dir(temp_dir)
		temp_dir.mkdir(parents=True)

		the_list = [1, 3.3, 'test', '🎈🎈🎈🎈🎈', True, False]
		the_tuple = list(the_list)
		the_dict = {'1': '🎈🎈🎈🎈🎈', 'two': the_list.copy()}
		the_list.append(the_dict)
		the_list.append(the_tuple)

		self.objects = the_list

		self.private_key, self.public_key = generate_keypair(4096)

	def tearDown(self):
		clean_dir(self.temp_dir)

	def test_encrypt_object(self):
		for msg in self.objects:
			cypher = encrypt_object(msg, self.public_key)
			self.assertNotEqual(msg, cypher)

	def test_encrypt_object_too_long(self):
		the_list = ['message'] * 100
		self.assertRaises(MessageTooLongForKey, encrypt_object, the_list, self.public_key)

	def test_encrypt_key_types(self):
		private_key_2, public_key_2 = generate_keypair(4096)
		for msg in self.objects:
			cypher = encrypt_object(msg, self.public_key)
			self.assertNotEqual(msg, cypher)

			cypher = encrypt_object(msg, self.private_key)
			self.assertNotEqual(msg, cypher)

			cypher = encrypt_object(msg, (public_key_2, self.public_key))
			self.assertNotEqual(msg, cypher)

			cypher = encrypt_object(msg, (self.private_key, private_key_2))
			self.assertNotEqual(msg, cypher)

	def test_decrypt_object(self):
		for msg in self.objects:
			cypher = encrypt_object(msg, self.public_key)
			self.assertNotEqual(msg, cypher)
			result = decrypt_object(cypher, self.private_key)
			self.assertEqual(msg, result)

			cypher = encrypt_object(msg, self.public_key)
			self.assertNotEqual(msg, cypher)
			result = decrypt_object(cypher, self.private_key)
			self.assertEqual(msg, result)

			cypher = encrypt_object(msg, self.private_key)
			self.assertNotEqual(msg, cypher)
			result = decrypt_object(cypher, self.private_key)
			self.assertEqual(msg, result)

			cypher = encrypt_object(msg, self.private_key)
			self.assertNotEqual(msg, cypher)
			# AttributeError: '_RSAPublicKey' object has no attribute 'decrypt'
			self.assertRaises(AttributeError, decrypt_object, cypher, self.public_key)

	def test_decrypt_key_types(self):
		msg = make_message(60)
		cypher = encrypt_string(msg, self.public_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		msg = make_message(60)
		cypher = encrypt_string(msg, self.private_key)
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, self.private_key)
		self.assertEqual(msg, result)

		private_key_2, public_key_2 = generate_keypair()

		msg = make_message(60)
		cypher = encrypt_string(msg, (public_key_2, self.public_key))
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, private_key_2)
		self.assertEqual(msg, result)
		# Was encrypted with newer key
		self.assertRaises(DecryptionFailed, decrypt_string, cypher, self.private_key)
		# Try key set
		result = decrypt_string(cypher, (self.private_key, private_key_2))
		self.assertEqual(msg, result)

		msg = make_message(60)
		cypher = encrypt_string(msg, (private_key_2, self.private_key))
		self.assertNotEqual(msg, cypher)
		result = decrypt_string(cypher, private_key_2)
		self.assertEqual(msg, result)
		# Was encrypted with newer key
		self.assertRaises(DecryptionFailed, decrypt_string, cypher, self.private_key)
		# Try key set
		result = decrypt_string(cypher, (self.private_key, private_key_2))
		self.assertEqual(msg, result)
