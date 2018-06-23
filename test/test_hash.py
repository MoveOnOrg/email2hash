import os
import sys
import filecmp
import unittest
import argparse

from email2hash import hash_email, parse_args

TEST_CSV = """id,first_name,last_name,email,ip_address
1,John,Doe,john@doe.com,127.233.246.121
2,John,Anon,anon@john.com,127.203.216.121
3,Bill,Smith,bill@smith.com,210.220.149.121
4,Nicolas,Bob,bob@nicolas.com,102.122.134.110
5,James,Bill,bill@james.org,91.211.21.203
"""


class TestHash(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("file")
        self.parser.add_argument("--output")
        self.parser.add_argument("--silent", action="store_true")
        self.parser.add_argument("--compress")

        self.file = os.path.dirname(__file__)

        self.test_input = os.path.join(self.file, "test_csv.csv")
        self.test_input_hashed = os.path.join(self.file, "test_csv.hashed")
        self.test_base_csv = os.path.join(self.file, "test_csv.test")

        with open(self.test_input, "w") as f:
            f.write(TEST_CSV)

    def test_simple_csv(self):
        hash_email(self.parser.parse_args(["--output",
                                           self.test_input_hashed,
                                           self.test_input, "--silent"]))
        self.assertTrue(filecmp.cmp(self.test_input_hashed,
                                    self.test_base_csv))

    def tearDown(self):
        os.remove(self.test_input)
        os.remove(self.test_input_hashed)


if __name__ == "__main__":
    unittest.main()
