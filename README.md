# hash.py: read a CSV file and hash the email addresses

### Introduction
This script reads a CSV file, hashes the email addresses using the SHA3-256 cryptographic hash function and outputs those hashes to a file.

The input CSV file should have a column with the header `email` in the first row that is used to determine the position of the email column for the subsequent rows. (The script does not make any attempt to guess an email address from a field.)

### Requirements

Python 3. No external libraries required.

### Usage

#### 1.Simple Usage
Assume a CSV file `test.csv` with the following contents:
```
id,first_name,last_name,email,ip_address
1,John,Doe,john@doe.com,127.233.246.121
2,John,Anon,anon@john.com,127.203.216.121
3,Bill,Smith,bill@smith.com,210.220.149.121
```
Run `hash.py` on the `test.csv`:

```
$ python3 hash.py test.csv 
Hashed 3 email addresses in 0.00 seconds using SHA3-256 to /home/example/test.hashed
$ cat test.hashed 
d3f44b5afda8361accde657bea3f982c022ceb37fdf0b43fe284f68bce2a0b9d
aaf5d07b496c9c2c71ef2c399b45b1d89e409f9fa6e51debb7bd0cc1be9793e6
de58838bf66241155f307ad1fa7da3a5ce0bffede555ae4bf90a385b4e9c9d56
```

#### 2. Advanced Options

For all supported options, run the script with `-h`:

```
$ python3 hash.py -h
usage: hash.py [-h] [-o out-file] [--silent] in-file

Read a CSV file and hash the email addresses.

positional arguments:
  in-file               input csv file with email addresses

optional arguments:
  -h, --help            show this help message and exit
  -o out-file, --output out-file
                        output file with hashed email addresses
  --silent              run in silent mode

```

###### Profiling

For a input file with 6400360 records (file size 378MB), the execution times on an Intel i5 2.30 GHz machine:

    Hashed 6400359 email addresses in 16.06 seconds using SHA3-256 to ...

(6400360 rows minus the first one which has the header.)

##### Output File

By default, the output file name will be the name of the input file with the `.hashed` extension. To change that, use the `-o` or `--output` argument:

```
$ python3 hash.py --output hashed.file test.csv
Hashed 3 email addresses in 0.00 seconds using SHA3-256 to /home/example/hashed.file
```

##### Verbosity

The script will output some execution information (line count, time taken and output file name) by default unless the `--silent` flag is specified.

```
$ python3 hash.py --output hashed.file --silent test.csv
The output file hashed.file exists and will be overwritten.
Proceed? (type yes or no): yes
```
##### CSV File Format

If you pass a *bad* CSV file with the missing `email` column, the script will just quit. Please fix the CSV file and run the script again. Refer to the CSV file example above for a sample input file.
