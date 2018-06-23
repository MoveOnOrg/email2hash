#! /usr/bin/env python3

"""Read a CSV file and hash the email addresses.

This script reads a CSV file, hashes the email addresses using a cryptographic
hash function (SHA3-256) and then outputs the hashes to another file.  The
script will output some execution information (line count, time taken and
output file name) by default unless the --silent flag is specified.
"""

import os
import sys
import time
import hashlib
import argparse


def hash_email(args):
    in_file, out_file = args.file, args.output

    # We note the executation start time; this is helpful for profiling.
    start_time = time.time()

    # No name given for an output file, so we create our own.
    if not out_file:
        in_file_name = os.path.splitext(os.path.basename(in_file))
        out_file = "{0}_hashed{1}".format(in_file_name[0], in_file_name[1])

    # Check if the output file exists and prompt the user. Do not prompt if
    # the --silent argument was passed and silently override.
    if not args.silent:
        if os.path.isfile(out_file):
            answer = input("The output file {0} exists and will be overwritten"
                           "\nProceed? (type yes or no): ".format(out_file))
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
                email_hash = hashlib.sha3_256()
                email_hash.update(email.encode("utf-8"))
                out.write(email_hash.hexdigest() + "\n")
    except IOError:
        sys.exit("File {0} not found. "
                 "Please check the file path.".format(in_file))

    # End of execution.
    end_time = time.time()

    if not args.silent:
        print("Hashed {0} email addresses in {1:0.2f} seconds using {2} "
              "to {3}".format(index, end_time - start_time, "SHA3-256",
                              os.path.abspath(out_file)))


def parse_args():
    parser = argparse.ArgumentParser(
            description="Read a CSV file and hash the email addresses."
            )
    parser.add_argument(
            "file",
            metavar="csv-file",
            help="input csv file with email addresses"
            )
    parser.add_argument(
            "-o", "--output",
            metavar="hash-file",
            help="output file with hashed email addresses"
            )
    parser.add_argument(
            "--silent",
            action="store_true",
            help="run in silent mode"
            )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    hash_email(args)
