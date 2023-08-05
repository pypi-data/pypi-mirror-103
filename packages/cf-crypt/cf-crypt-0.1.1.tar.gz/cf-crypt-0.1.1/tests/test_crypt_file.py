import io
import struct
import sys
from unittest import TestCase
import random

from cfcrypt.crypt_file import CryptFileBinaryIO, CryptFileTextIO
from cfcrypt.constants import ALGO_MODE_CBC
from cfcrypt.rsa import generate_keypair
from cfcrypt.rsa.exceptions import DecryptionFailed, InvalidSignature

from pathlib import Path
if sys.version_info[:2] <= (3, 7):
	from pathlib3x import Path


def random_data(n=1024 ** 2):
	# random.randbytes(n)  # 3.9 feature
	return bytearray(random.getrandbits(8) for _ in range(n))


class TestCryptFileBinaryIO(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.private_key, cls.public_key = generate_keypair()
		cls.filename = Path('./test.kenc')

	def tearDown(self):
		self.filename.unlink(missing_ok=True)

	def test_round_trip(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	def test_big_round_trip(self):
		test = random_data(8 * 1024 ** 2)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	def test_partial_read(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read(16)

			self.assertEqual(test[:16], round_trip_test)

	def test_sequential_partial_read(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read(16)

			self.assertEqual(test[:16], round_trip_test)
			round_trip_test = fh.read(16)
			self.assertEqual(test[16:32], round_trip_test)

	def test_seek_read(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			fh.seek(512)
			round_trip_test = fh.read(16)
			self.assertEqual(test[512:512 + 16], round_trip_test)

	def test_reopen_round_trip(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()
			self.assertEqual(test, round_trip_test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()
			self.assertEqual(test, round_trip_test)

	def test_wrong_key(self):
		test = random_data(1024)

		bad_private_key, bad_public_key = generate_keypair()

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		self.assertRaises(DecryptionFailed, CryptFileBinaryIO, self.filename, 'rb', bad_private_key, bad_private_key)

	def test_tamping_with_parameter(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		# Change a field in the header
		with open(self.filename, 'rb+') as fh:
			fh.seek(6)
			fh.write(struct.pack('<B', ALGO_MODE_CBC))

		self.assertRaises(RuntimeError, CryptFileBinaryIO, self.filename, 'rb', self.private_key, self.private_key)

	def test_tamping_with_data(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		# Change a field in the header
		with open(self.filename, 'rb+') as fh:
			fh.seek(512)
			fh.write(struct.pack('<B', 9))

		self.assertRaises(InvalidSignature, CryptFileBinaryIO, self.filename, 'rb', self.private_key, self.private_key)

	def test_round_trip_multi_key(self):
		test = random_data(1024)
		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileBinaryIO(self.filename, 'wb', keys, keys) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', keys, keys) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	def test_round_trip_new_key(self):
		test = random_data(1024)
		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', keys, keys) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	# def unsupported_modes_in_file_header(self):
	# 	test = random_data(1024)
	# 	new_private_key, new_public_key = generate_keypair()
	# 	keys = new_private_key, self.private_key
	#
	# 	with CryptFileBinaryIO(self.filename, 'wb', keys, keys) as fh:
	# 		fh.write(test)

	def test_unsupported_write_to_finalized(self):
		test = random_data(1024)
		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileBinaryIO(self.filename, 'wb', keys, keys) as fh:
			fh.write(test)
			fh.finalize()

			# raise io.UnsupportedOperation('This file has already been finalized.')
			self.assertRaises(io.UnsupportedOperation, fh.finalize)

			# raise io.UnsupportedOperation('This file has already been finalized.')
			self.assertRaises(io.UnsupportedOperation, fh.write, b'junk data')

		with CryptFileBinaryIO(self.filename, 'rb', keys, keys) as fh:
			# io.UnsupportedOperation('This file is not open write mode.')
			self.assertRaises(io.UnsupportedOperation, fh.finalize)

	def test_unsupported_text_io(self):
		text = """Cryptography, or cryptology (from Ancient Greek: κρυπτός, romanized: kryptós "hidden, secret"; and 
		γράφειν graphein, "to write", or -λογία -logia, "study", respectively[1]), is the practice and study of 
		techniques for secure communication in the presence of third parties called adversaries.[2] More generally, 
		cryptography is about constructing and analyzing protocols that prevent third parties or the public from 
		reading private messages;[3] various aspects in information security such as data confidentiality, 
		data integrity, authentication, and non-repudiation[4] are central to modern cryptography. Modern cryptography 
		exists at the intersection of the disciplines of mathematics, computer science, electrical engineering, 
		communication science, and physics. Applications of cryptography include electronic commerce, chip-based 
		payment cards, digital currencies, computer passwords, and military communications."""

		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileTextIO(self.filename, keys, keys, 'w', encoding='utf-8') as fh:
			fh.write(text)

		with CryptFileTextIO(self.filename, keys, keys, 'r', encoding='utf-8') as fh:
			decoded_text = fh.read()

		self.assertEqual(text, decoded_text)

	def test_unsupported_text_io_arguments(self):
		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileTextIO(self.filename, keys, keys, 'w', encoding='utf-8') as fh:
			fh.write('text')

		self.assertRaises(TypeError, CryptFileTextIO, self.filename, keys, None)
		self.assertRaises(TypeError, CryptFileTextIO, self.filename, None, keys)
		self.assertRaises(io.UnsupportedOperation, CryptFileTextIO, self.filename, keys, keys, 'r+')
