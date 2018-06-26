#! /usr/bin/env python3
#
# BSD 3-Clause License
# Copyright (c) 2018, 'Layer 8, LLC'. All rights reserved.

"""Read a CSV file and hash the email addresses.

This script reads a CSV file, hashes the email addresses using an HMAC
(SHA3-256) and then outputs the hashes to another file.  The script will
output some execution information (line count, time taken and output file
name) by default unless the --silent flag is specified.

For more information about the design of the script, refer to the
specifications file email2hash-spec.txt.
"""

import os
import sys
import time
import hmac
import getpass
import zipfile
import hashlib
import argparse


def get_secret():
    while True:
        secret = getpass.getpass("Enter the secret key: ")
        if not secret:
            print("! I need a secret to continue.")
            continue
        # This is arbitrary; ideally the length should be at least 32 bytes
        # but we need to enforce a number.
        if len(secret) < 10:
            print("! Please choose a secret longer than 10 characters.")
            continue
        confirm = getpass.getpass("Enter the same key again to confirm: ")
        if not secret == confirm:
            print("! Your secret key did not match. Let's try again.")
            continue
        break
    return secret


def hash_email(args):
    in_file = args.file

    # We note the executation start time; this is helpful for profiling.
    start_time = time.time()

    # out_file refers to the name of the output file with _hashed added to it.
    # out_file_zip refers to the name of the ZIP file.
    # output_file decides which file to output, CSV or ZIP.
    in_file_name = os.path.splitext(os.path.basename(in_file))
    out_file = "{0}_hashed{1}".format(in_file_name[0], in_file_name[1])
    if args.compress:
        out_file_zip = "{0}_hashed{1}".format(in_file_name[0], ".zip")
    output_file = out_file_zip if args.compress else out_file

    # Check if the output file exists and prompt the user. Do not prompt if
    # the --silent argument was passed and silently override.
    if not args.silent:
        if os.path.isfile(output_file):
            answer = input("The output file {0} exists and will be overwritten"
                           "\nProceed? (type yes or no): ".format(output_file))
            if answer not in ("yes", "y"):
                sys.exit()

    # Input the secret key from the user.
    secret = get_secret()

    if not args.silent:
        print("Please wait, hashing email addresses. This may take a while...")

    hashed_emails = []
    try:
        with open(in_file, "r") as f:
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
            # line, hash the email address and append it to the list.
            # Note that we do not use csvreader and that's by design -- we
            # don't need the overhead and it performs a lot worse.
            for index, line in enumerate(f, 1):
                email = line.split(",")[email_index].strip()
                email_hash = hmac.new(secret.encode("utf-8"),
                                      email.encode("utf-8"),
                                      hashlib.sha3_256)
                hashed_emails.append(email_hash.hexdigest())
    except IOError:
        sys.exit("File {0} not found. "
                 "Please check the file path.".format(in_file))

    # Sort the list and write it to the file.
    hashed_emails.sort()
    with open(out_file, "w") as f:
        for email in hashed_emails:
            f.write("{0}\n".format(email))

    # If --compress was passed, compress the output file using ZIP.
    if args.compress:
        with zipfile.ZipFile(out_file_zip, 'w', zipfile.ZIP_DEFLATED) as fzip:
            fzip.write(out_file)

    # End of execution.
    end_time = time.time()

    if not args.silent:
        print("Hashed {0} email addresses in {1:0.2f} seconds using {2} "
              "to {3}".format(index, end_time - start_time,
                              "HMAC (SHA3-256)", output_file))


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
            "--compress",
            action="store_true",
            help="compress the output file (create a ZIP archive)"
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
