#! /usr/bin/env python3

"""Read a CSV file and hash the email addresses.

This script reads a CSV file, hashes the email addresses using a cryptographic
hash function (configurable) and then outputs the hashes to another file. The
default hash function is SHA1 but SHA256 and BLAKE2 are also supported via the
arguments. The script will output some execution information (line count, time
taken and output file name) by default unless the --silent flag is specified.
"""

import os
import sys
import time
import hashlib
import argparse


def hash_email(args):
    in_file, out_file = args.file, args.output

    hashes = {
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "blake2s": hashlib.blake2s,
            "blake2b": hashlib.blake2b
            }

    # We note the executation start time; this is helpful for profiling.
    start_time = time.time()

    # No name given for an output file, so we create our own.
    if not out_file:
        out_file = "{0}.hashed".format(
                os.path.splitext(os.path.basename(in_file))[0])

    # Check if the output file exists and prompt the user.
    if os.path.isfile(out_file):
        answer = input("The output file {0} exists and will be overwritten.\n"
                       "Proceed? (type yes or no): ".format(out_file))
        if answer not in ("yes", "y"):
            sys.exit()

    try:
        with open(in_file, "r") as f, open(out_file, "w") as out:
            # The first line is the header. If it is not or if it is missing
            # the email column, we have a CSV file that we don't know how to
            # process, so quit.
            try:
                first_line = f.readline().split(",")
                email_index = first_line.index("email")
            except ValueError:
                sys.exit("Error: unable to find column 'email' in "
                         "input file {0}".format(os.path.abspath(in_file)))

            # We know the position of the email column, so use it to split the
            # line, hash the email address and save it to the output file.
            # Note that we do not use csvreader and that's by design -- we
            # don't need the overhead and it performs a lot worse.
            for index, line in enumerate(f, 1):
                email = line.split(",")[email_index].strip()
                email_hash = hashes[args.hash]()
                email_hash.update(email.encode("utf-8"))
                out.write(email_hash.hexdigest() + "\n")
    except IOError:
        sys.exit("File {0} not found. "
                 "Please check the file path.".format(in_file))

    # End of execution.
    end_time = time.time()

    if not args.silent:
        print("Hashed {0} email addresses in {1:0.2f} seconds using {2} "
              "to {3}".format(index, end_time - start_time, args.hash,
                              os.path.abspath(out_file)))


def parse_args():
    parser = argparse.ArgumentParser(
            description="Read a CSV file and hash the email addresses."
            )
    parser.add_argument(
            "file",
            metavar="in-file",
            help="input csv file with email addresses"
            )
    parser.add_argument(
            "-o", "--output",
            metavar="out-file",
            help="output file with hashed email addresses"
            )
    parser.add_argument(
            "--hash",
            choices=("sha1", "sha256", "blake2s", "blake2b"),
            default="sha256",
            help="cryptographic hash function (default: %(default)s)")
    parser.add_argument(
            "--silent",
            action="store_true",
            help="run in silent mode"
            )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    hash_email(args)
