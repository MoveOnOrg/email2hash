import os
import sys
import getpass
import filecmp
import unittest
import argparse

from unittest.mock import patch

from email2hash import hash_email, parse_args, diceware_word

TEST_CSV = """id,first_name,last_name,email,ip_address
1,John,Doe,john@doe.com,127.233.246.121
2,John,Anon,anon@john.com,127.203.216.121
3,Bill,Smith,bill@smith.com,210.220.149.121
4,Nicolas,Bob,bob@nicolas.com,102.122.134.110
5,James,Bill,bill@james.org,91.211.21.203
"""


class TestHash(unittest.TestCase):
    @patch("getpass.getpass")
    def test_simple_csv(self, secret):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("file")
        self.parser.add_argument("--silent", action="store_true")
        self.parser.add_argument("--compress")

        self.file = os.path.dirname(__file__)

        self.test_input = os.path.join(self.file, "testfile.csv")
        self.test_input_hashed = os.path.join(self.file, "testfile_hashed.csv")
        self.test_base_csv = os.path.join(self.file, "test_hashed.csv")

        with open(self.test_input, "w") as f:
            f.write(TEST_CSV)

        # Do not use this secret; set your own by running email2hash.py
        secret.return_value = "a really long secret"
        os.chdir("test")
        hash_email(self.parser.parse_args([self.test_input, "--silent"]))
        self.assertTrue(filecmp.cmp(self.test_input_hashed,
                                    self.test_base_csv))
        os.remove(self.test_input)
        os.remove(self.test_input_hashed)

    def test_diceword(self):
        self.words = diceware_word().split()
        self.word_list = ["overcrowd", "ladle", "disdain", "falcon", "varsity"]
        self.assertEqual(len(self.word_list), len(self.words),
                         msg="Diceware word list returned unequal word length")


if __name__ == "__main__":
    unittest.main()
