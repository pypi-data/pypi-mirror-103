import io
import re
import stat
import sys
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch
from tempfile import TemporaryDirectory

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from cfcrypt.keyring.keyring import KeyRing, password_generator, MetaKeyRing
import os

from cfcrypt.rsa import generate_keypair, private_key_to_pem_file, private_key_to_pem


class SuppressStdout(object):

    def __enter__(self):
        # Suppress stdout
        suppress_text = io.StringIO()
        self.active_stdout = sys.stdout
        sys.stdout = suppress_text
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.active_stdout


def clean_dir(temp_dir):
    if temp_dir.exists():
        for filename in temp_dir.iterdir():
            os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
            filename.unlink()
        temp_dir.rmdir()
    temp_dir.mkdir(parents=True)


class TestKeyRingBaseCreation(TestCase):

    def setUp(self):
        temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
        clean_dir(temp_dir)
        self.patcher = patch('os.environ', {"CRYPT_KEYRING": str(temp_dir)})
        self.mock_foo = self.patcher.start()

    def tearDown(self):
        try:
            temp_dir = Path(self.temp_dir)
            for filename in temp_dir.iterdir():
                os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
                filename.unlink()
            temp_dir.rmdir()
        finally:
            self.patcher.stop()

    def test_create_key_ring_env(self):
        user_password = 'password'

        # RuntimeError('KeyRing path not set in environment variable CRYPT_KEYRING')
        del os.environ['CRYPT_KEYRING']
        self.assertRaises(RuntimeError, KeyRing.create_key_ring, user_password)

    def test_create_key_ring_supplied_password(self):
        user_password = "password"

        with SuppressStdout():
            # RuntimeError('KeyRing path not set in environment variable CRYPT_KEYRING')
            keyring = KeyRing.create_key_ring(user_password)
            self.assertIsInstance(keyring, KeyRing)

            keyfile = keyring.main_key_file()
            self.assertTrue(keyfile.exists())

            keyring_file = keyring.cache_file
            self.assertTrue(keyring_file.exists())

            # RuntimeError('Cannot create a new key ring as one already exists here: {}'.format(kek_path))
            self.assertRaises(RuntimeError, KeyRing.create_key_ring, user_password)

    def test_create_key_ring_generated_password(self):

        with SuppressStdout():
            keyring = KeyRing.create_key_ring()
            self.assertIsInstance(keyring, KeyRing)

            keyfile = keyring.main_key_file()
            self.assertTrue(keyfile.exists())

            keyring_file = keyring.cache_file
            self.assertTrue(keyring_file.exists())

    def test_singleton(self):
        user_password = "password"

        with SuppressStdout():
            created_keyring = KeyRing.create_key_ring(user_password)
            self.assertIsInstance(created_keyring, KeyRing)

        loaded_keyring = KeyRing(password=user_password)
        self.assertIsInstance(loaded_keyring, KeyRing)

        self.assertIs(created_keyring, loaded_keyring)

    def test_bad_password(self):
        user_password = "password"

        with SuppressStdout():
            created_keyring = KeyRing.create_key_ring(user_password)
            self.assertIsInstance(created_keyring, KeyRing)

        # bad password
        self.assertRaises(ValueError, KeyRing, password='bdbfdbf')
        # No password
        self.assertRaises(TypeError, KeyRing, password=None)

    def test_env_password(self):
        user_password = "password"
        patcher = patch('os.environ', {"CRYPT_KEYRING": str(self.temp_dir), "CRYPT_KEYRING_TOKEN": user_password})
        patcher.start()
        try:
            with SuppressStdout():
                created_keyring = KeyRing.create_key_ring(user_password)
            self.assertIsInstance(created_keyring, KeyRing)

            loaded_keyring = KeyRing()
            self.assertIsInstance(loaded_keyring, KeyRing)

            self.assertIs(created_keyring, loaded_keyring)
        finally:
            patcher.stop()


class TestKeyRingBase(TestCase):

    def setUp(self):
        temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
        clean_dir(temp_dir)

        self.password = "password"
        self.patcher = patch('os.environ', {"CRYPT_KEYRING": str(self.temp_dir), "CRYPT_KEYRING_TOKEN": self.password})
        self.mock_foo = self.patcher.start()

        with SuppressStdout():
            self.keyring = KeyRing.create_key_ring(self.password)

    def tearDown(self):
        try:
            temp_dir = Path(self.temp_dir)
            for filename in temp_dir.iterdir():
                os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
                filename.unlink()
            temp_dir.rmdir()
        finally:
            self.patcher.stop()

    def test_change_password(self):
        new_password = self.password + '2'
        self.keyring.change_password(self.password, new_password)

        keyring = KeyRing(password=new_password)
        self.assertIsInstance(keyring, KeyRing)

        # Bad password
        self.assertRaises(ValueError, KeyRing, password=self.password)

    def test_directory(self):
        self.assertEqual(str(KeyRing.directory()), os.environ["CRYPT_KEYRING"])
        self.assertTrue(KeyRing.directory().exists())

    def test_main_key_file(self):
        self.assertTrue(KeyRing.main_key_file().exists())
        self.assertEqual(KeyRing.main_key_file().suffix, '.pem')

    def test_load(self):
        # Clean out the singleton to simulate a fresh load
        self.keyring = None
        MetaKeyRing._instances = {}
        keyring = KeyRing()
        self.assertIsInstance(keyring, KeyRing)

        key_name = 'mark'
        created_key = keyring.create_key(key_name)

        # Clean out the singleton to simulate a fresh load
        del keyring
        MetaKeyRing._instances = {}

        # Check the key persisted
        keyring = KeyRing()
        self.assertIsInstance(keyring, KeyRing)
        returned_key = keyring.get_key(key_name)
        self.assertEqual(private_key_to_pem(created_key), private_key_to_pem(returned_key))


class TestKeyRing(TestCase):

    def setUp(self):
        temp_dir = self.temp_dir = Path('./tmp_9_7kuse')
        clean_dir(temp_dir)

        self.password = "password"
        self.patcher = patch('os.environ', {"CRYPT_KEYRING": str(self.temp_dir), "CRYPT_KEYRING_TOKEN": self.password})
        self.mock_foo = self.patcher.start()

        with SuppressStdout():
            self.keyring = KeyRing.create_key_ring(self.password)

    def tearDown(self):
        try:
            temp_dir = Path(self.temp_dir)
            for filename in temp_dir.iterdir():
                os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)
                filename.unlink()
            temp_dir.rmdir()
        finally:
            self.patcher.stop()

    def test_namespace(self):
        self.assertEqual(self.keyring.namespace, 'default')

        namespace = 'test_namespace'
        self.keyring.set_namespace(namespace)
        self.assertEqual(self.keyring.namespace, namespace)

        namespace = 'test_namespace2'
        self.keyring.set_namespace(namespace)
        self.assertEqual(self.keyring.namespace, namespace)

        namespace = ''
        self.keyring.set_namespace(namespace)
        self.assertEqual(self.keyring.namespace, namespace)

        namespace = 'default'
        self.keyring.set_namespace(namespace)
        self.assertEqual(self.keyring.namespace, namespace)

    def test_attach_key(self):
        key_name = 'fred'
        private_key, public_key = generate_keypair()
        return_private_key = self.keyring.attach_key(key_name, private_key)
        self.assertIs(private_key, return_private_key)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(private_key, return_private_key)

        namespace = 'test_namespace'
        return_private_key = self.keyring.attach_key(key_name, private_key, namespace)
        self.assertIs(private_key, return_private_key)
        return_private_key = self.keyring.get_key(key_name, namespace)
        self.assertIs(private_key, return_private_key)

        namespace = 'test_namespace'
        key_name = 'joe'
        return_private_key = self.keyring.attach_key(key_name, private_key, namespace)
        self.assertIs(private_key, return_private_key)

        # Valid key name, wrong namespace.
        self.assertRaises(KeyError, self.keyring.get_key, key_name, 'default')

    def test_attach_key_file(self):
        key_path = self.temp_dir / 'test.pem'
        private_key, public_key = generate_keypair()
        private_key_to_pem_file(key_path, private_key)

        key_name = 'fred'
        return_private_key = self.keyring.attach_key_file(key_name, key_path)
        self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(return_private_key))
        return_private_key = self.keyring.get_key(key_name)
        self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(return_private_key))

        key_password = 'password'
        private_key_to_pem_file(key_path, private_key, key_password)

        key_name = 'fred'
        return_private_key = self.keyring.attach_key_file(key_name, key_path, key_password)
        self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(return_private_key))
        return_private_key = self.keyring.get_key(key_name)
        self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(return_private_key))

        # Un needed password
        self.assertRaises(ValueError, self.keyring.attach_key_file, key_name, key_path, 'bad password')

        key_password = 'password'
        private_key_to_pem_file(key_path, private_key, key_password)

        # Bad password
        self.assertRaises(ValueError, self.keyring.attach_key_file, key_name, key_path, 'bad password')
        # No password
        self.assertRaises(TypeError, self.keyring.attach_key_file, key_name, key_path)

    def test_create_key(self):
        key_name = 'mike'
        created_private_key = self.keyring.create_key(key_name)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(created_private_key, return_private_key)

        namespace = 'blah'
        created_private_key = self.keyring.create_key(key_name, namespace)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name, namespace)
        self.assertIs(created_private_key, return_private_key)

        # No namespace
        key_name = 'sally'
        self.keyring.create_key(key_name, namespace)
        self.assertRaises(KeyError, self.keyring.get_key, key_name)

    def test_delete_key(self):
        key_name = 'megan'
        created_private_key = self.keyring.create_key(key_name)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(created_private_key, return_private_key)

        self.keyring.delete_key(key_name, 'default')
        self.assertRaises(KeyError, self.keyring.get_key, key_name)

        namespace = 'melbourne'
        created_private_key = self.keyring.create_key(key_name, namespace)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name, namespace)
        self.assertIs(created_private_key, return_private_key)

        # Wrong namespace
        self.assertRaises(KeyError, self.keyring.delete_key, key_name, 'default')

        self.keyring.delete_key(key_name, namespace)
        self.assertRaises(KeyError, self.keyring.get_key, key_name, namespace)

    def test_roll_key(self):
        key_name = 'alex'
        created_private_key = self.keyring.create_key(key_name)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(created_private_key, return_private_key)

        new_private_key = self.keyring.roll_key(key_name)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(new_private_key, return_private_key)
        self.assertIsNot(created_private_key, return_private_key)

        namespace = 'tāupo'
        created_private_key = self.keyring.create_key(key_name, namespace)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name, namespace)
        self.assertIs(created_private_key, return_private_key)

        new_private_key = self.keyring.roll_key(key_name, namespace)
        return_private_key = self.keyring.get_key(key_name, namespace)
        self.assertIs(new_private_key, return_private_key)
        self.assertIsNot(created_private_key, return_private_key)

        # Wrong namespace
        self.assertRaises(KeyError, self.keyring.roll_key, key_name, 'nelson')

        # Triple roll
        key_name = 'james'
        created_private_key = self.keyring.create_key(key_name)
        self.assertIsInstance(created_private_key, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(created_private_key, return_private_key)

        new_private_key = self.keyring.roll_key(key_name)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(new_private_key, return_private_key)
        self.assertIsNot(created_private_key, return_private_key)

        new_private_key = self.keyring.roll_key(key_name)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(new_private_key, return_private_key)
        self.assertIsNot(created_private_key, return_private_key)

    def test_get_key(self):
        # Tested above in the rest of the tests
        pass

    def test_get_keys(self):

        # Triple roll
        key_name = 'marian'
        private_key_a = self.keyring.create_key(key_name)
        self.assertIsInstance(private_key_a, RSAPrivateKey)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(private_key_a, return_private_key)

        private_key_b = self.keyring.roll_key(key_name)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(private_key_b, return_private_key)
        self.assertIsNot(private_key_a, return_private_key)

        private_key_c = self.keyring.roll_key(key_name)
        return_private_key = self.keyring.get_key(key_name)
        self.assertIs(private_key_c, return_private_key)
        self.assertIsNot(private_key_a, return_private_key)

        private_key_set = self.keyring.get_keys(key_name)
        self.assertIsInstance(private_key_set, tuple)
        self.assertIs(private_key_set[0], private_key_c)
        self.assertIs(private_key_set[1], private_key_b)
        self.assertIs(private_key_set[2], private_key_a)


class Test(TestCase):

    def test_password_generator(self):

        import random
        random.seed(0)

        # Replace the secure system random of secrets.choice with a deterministic random for testing.
        with patch('secrets.choice', random.choice):
            seen = set()
            length = 60
            for _ in range(25000):
                output = password_generator(length)
                self.assertEqual(len(output), length)
                self.assertTrue(re.search(r'\d+', output))
                self.assertTrue(re.search(r'[a-z]+', output))
                self.assertTrue(re.search(r'[A-Z]+', output))
                self.assertTrue(re.search(r'[!#$%&*+\-?@_~]+', output))

                self.assertNotIn(output, seen)
                seen.add(output)
