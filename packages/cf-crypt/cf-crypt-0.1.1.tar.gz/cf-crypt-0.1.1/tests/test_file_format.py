import os
import stat
import struct
from pathlib import Path
from unittest import TestCase

from cfcrypt import FileParserError
from cfcrypt.file_format import ContainerFormat, is_crypt_file, ContainerFormatV1


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

    def tearDown(self):
        clean_dir(self.temp_dir)

    def test_is_crypt_file(self):
        filename = self.temp_dir / 'test.crpt'
        self.assertRaises(FileNotFoundError, is_crypt_file, filename)

        with open(filename, 'wb') as fh:
            fh.write(ContainerFormat.magic_bytes)
        self.assertTrue(is_crypt_file(filename))

        filename = self.temp_dir / 'test.crpt'
        with open(filename, 'wb') as fh:
            fh.write(b'not magic bytes')
        self.assertFalse(is_crypt_file(filename))

    def test_create_from_file(self):
        filename = self.temp_dir / 'test.crpt'
        self.assertRaises(FileNotFoundError, is_crypt_file, filename)

        with filename.open('wb') as fh:
            fh.write(ContainerFormat.magic_bytes)
            fh.write(struct.pack('B', 1))

        with filename.open('rb') as fh:
            # RuntimeError: Failed to read the whole header.
            self.assertRaises(RuntimeError, ContainerFormat.create_from_file, fh)

    def test_get_version_class(self):
        filename = self.temp_dir / 'test.crpt'
        self.assertRaises(FileNotFoundError, is_crypt_file, filename)

        with filename.open('wb') as fh:
            fh.write(struct.pack('<4sB', ContainerFormat.magic_bytes, 1))
            fh.write(b'other junk')
        with filename.open('rb') as fh:
            cls = ContainerFormat.get_version_class(fh)
            self.assertIs(cls, ContainerFormatV1)

        with filename.open('wb') as fh:
            fh.write(struct.pack('<4sB', ContainerFormat.magic_bytes, 22))
            fh.write(b'other junk')
        with filename.open('rb') as fh:
            # FileParserError: Unknown version number. The file could be corrupt, or created by a newer version of
            # this software.
            self.assertRaises(FileParserError, ContainerFormat.get_version_class, fh)

        with filename.open('wb') as fh:
            fh.write(struct.pack('<4sB', b'bang', 22))
            fh.write(b'other junk')
        with filename.open('rb') as fh:
            # FileParserError: 'Bad magic number'
            self.assertRaises(FileParserError, ContainerFormat.get_version_class, fh)
