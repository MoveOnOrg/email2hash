# email2hash.py: read a CSV file and hash the email addresses

### Introduction
This script reads a CSV file, hashes the email addresses using HMAC (SHA3-256) and outputs those hashes to a file.

The input CSV file should have a column with the header `email` in the first row that is used to determine the position of the email column for the subsequent rows. (The script does not make any attempt to guess an email address from a field.)

### Requirements

Python 3. No external libraries required.

### Usage

#### 1. Simple Usage
Assume a CSV file `email_list.csv` with the following contents:
```
id,first_name,last_name,email,ip_address
1,John,Doe,john@doe.com,127.233.246.121
2,John,Anon,anon@john.com,127.203.216.121
3,Bill,Smith,bill@smith.com,210.220.149.121
```
Run `email2hash.py` on the `email_list.csv`:

```
$ python3 email2hash.py email_list.csv 
Enter the secret key:
Enter the same key again to confirm:
Please wait, hashing email addresses. This may take a while...
Hashed 3 email addresses in 5.59 seconds using HMAC (SHA3-256) to email_list_hashed.csv
```
(Secret in the above example: `this is a secret`)
```
$ cat email_list_hashed.csv
42d66628b7ca816a5558877c3a810f9c55a64a9b53021516884cf10c1228680e
80523abe9c7220be7848f6eba78ff830d3dfaa0bc9aaa712bcbabf5a12a5537f
a311fd21ae832bbf1f1d9616c5168befdde75642bf943cc4fd53182ac11f5e41
```

#### 2. Advanced Options

For all supported options, run the script with `-h`:

```
$ python3 email2hash.py -h
usage: email2hash.py [-h] [--compress] [--silent] csv-file

Read a CSV file and hash the email addresses.

positional arguments:
  csv-file    input csv file with email addresses

optional arguments:
  -h, --help  show this help message and exit
  --compress  compress the output file (create a ZIP archive)
  --silent    run in silent mode

```

###### Compression

If you pass the `--compress` argument, the script compresses the output file and creates a ZIP archive. This is helpful in saving space and the difference can be substantial depending on the size of the input file.

###### Profiling

For an input file (378MB) with 6400360 records, the execution times on an Intel i5 2.30 GHz machine:

    Hashed 6400357 email addresses in 58.18 seconds using HMAC (SHA3-256) to email_list_hashed.csv

(6400360 rows minus the first one which has the header.)

##### Output File

By default, the output file name will be the name of the input file with `_hashed` added to it; so if the input file is `email_list.csv`, the output file will be `email_list_hashed.csv`. If the `--compress` flag as passed, the output file name will have the name of the input file with `_hashed.zip` added to it.

```
$ python3 email2hash.py email_list.csv 
Hashed 10 email addresses in 4.95 seconds using HMAC (SHA3-256) to email_list_hashed.csv

$ python3 email2hash.py email_list.csv --compress
Hashed 10 email addresses in 3.48 seconds using HMAC (SHA3-256) to email_list_hashed.zip
```

##### Verbosity

The script will output some execution information (line count, time taken and output file name) by default unless the `--silent` flag is specified.

```
$ python3 email2hash.py email_list.csv --compress --silent
Enter the secret key: 
Enter the same key again to confirm: 
```

As in the above example, it will still ask you for the secret key because that's required and cannot be inferred from the script arguments.

Note: When running in `--silent`, the script will override any existing output file without confirming.

##### CSV File Format

If you pass a *bad* CSV file with the missing `email` column, the script will just quit. Please fix the CSV file and run the script again. Refer to the CSV file example above for a sample input file.

### Developers: Testing

We just have two (simple) tests currently that test the functionality of the script:

```
$ python3 -m unittest discover -v test
test_diceword (test_hash.TestHash) ... ok
test_simple_csv (test_hash.TestHash) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.005s

OK
```
