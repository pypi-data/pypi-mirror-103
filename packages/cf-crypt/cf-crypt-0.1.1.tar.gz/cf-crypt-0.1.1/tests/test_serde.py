import os
import stat
import sys
from unittest import TestCase

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from cfcrypt.rsa import generate_private_key, private_key_to_pem, rsa_private_key_decode, rsa_private_key_encode

from pathlib import Path
if sys.version_info[:2] <= (3, 7):
	from pathlib3x import Path


def clean_dir(temp_dir):
	if temp_dir.exists():
		for filename in temp_dir.iterdir():
			os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
			filename.unlink()
		temp_dir.rmdir()


class Test(TestCase):

	def setUp(self):
		temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
		clean_dir(temp_dir)
		temp_dir.mkdir(parents=True)

		self.private_key = generate_private_key()
		self.private_key_pem = private_key_to_pem(self.private_key)

	def tearDown(self):
		clean_dir(self.temp_dir)

	def test_rsa_private_key_decode(self):
		blob = {
			'__json_type__': '_RSAPrivateKey',
			'private_key': self.private_key_pem.decode('utf-8')
		}
		result = rsa_private_key_decode(blob)
		self.assertIsInstance(result, RSAPrivateKey)
		self.assertEqual(private_key_to_pem(result), self.private_key_pem)

	def test_rsa_private_key_encode(self):
		blob = {
			'__json_type__': '_RSAPrivateKey',
			'private_key': self.private_key_pem.decode('utf-8')
		}
		result = rsa_private_key_encode(self.private_key)
		self.assertEqual(result, blob)

	def test_round_trip(self):
		out_private_key = rsa_private_key_decode(rsa_private_key_encode(self.private_key))
		self.assertEqual(self.private_key_pem, private_key_to_pem(out_private_key))

	def test_rsa_private_key_decode_bad_type(self):
		blob = {
			'__json_type__': 'BadType',
			'rsa_private_key': '2021-04-07T00:00:08.114099'
		}
		self.assertRaises(TypeError, rsa_private_key_decode, blob)

	def test_rsa_private_key_decode_bad_blob(self):
		blob = {
			'rsa_private_key': '2021-04-07T00:00:08.114099'
		}
		self.assertRaises(KeyError, rsa_private_key_decode, blob)
		blob = {}
		self.assertRaises(KeyError, rsa_private_key_decode, blob)
