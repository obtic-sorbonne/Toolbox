import unittest

from todh import __version__


class BasicTestCase(unittest.TestCase):
    def test_version(self):
        assert __version__ == '0.1.0'


if __name__ == '__main__':
    unittest.main()
