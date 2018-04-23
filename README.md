# hash.py: read a CSV file and hash the email addresses

### Introduction
This script reads a CSV file, hashes the email addresses using the specified cryptographic hash function and outputs those hashes to a file.

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
Hashed 3 email addresses in 0.00 seconds using sha256 to /home/example/test.hashed
$ cat test.hashed 
d709f370e52b57b4eb75f04e2b3422c4d41a05148cad8f81776d94a048fb70af
fdeeba79c3bb0348f9ac311909b56bf7e1891fe6f4e0793e82cc26abb181e8ed
c78310110ff5433fb24caf8dfd2728e6c54d71e9007bafaae71877d4b944afcb
```

#### 2. Advanced Options

For all supported options, run the script with `-h`:

```
$ python3 hash.py -h
usage: hash.py [-h] [-o out-file] [--hash {sha1,sha256,blake2s,blake2b}]
               [--silent]
               in-file

Read a CSV file and hash the email addresses.

positional arguments:
  in-file               input csv file with email addresses

optional arguments:
  -h, --help            show this help message and exit
  -o out-file, --output out-file
                        output file with hashed email addresses
  --hash {sha1,sha256,blake2s,blake2b}
                        cryptographic hash function (default: sha256)
  --silent              run in silent mode
```

##### Hash

You can specify a different hash (the default is `SHA-256`) with the `--hash' argument; the supported hashes are `SHA-1`, `SHA-256`, `BLAKE2s`, `BLAKE2b`. 

```
$ python3 hash.py --hash sha1 test.csv 
The output file test.hashed exists and will be overwritten.
Proceed? (type yes or no): yes
Hashed 3 email addresses in 2.39 seconds using sha1 to /home/example/test.hashed
```

You can profile which hash works the best for you but without going into detail, the length of the hash (hexadecimal) varies depending on the hash function you use:

| Hash      | Length (Output) |
| --------- | --------------- |
| SHA-1     |  40 (20 bytes)  |
| SHA-256   |  64 (32 bytes)  |
| BLAKE2s   |  64 (32 bytes)  |
| BLAKE2b   |  128 (64 bytes) |

We recommend that you use the default (`SHA-256`) or either `BLAKE2s` or `BLAKE2b`, depending on the length of the digest you want.

Here is the difference between the hashes, for the same input file.

```
SHA-1
fd9c796f4269b3484f9ef436627d0d1cb35071c5
05780e69ea093e5300c973e38e80878f7db27a79
9950e9b13113a223c5095426f240b323f4a7f217

```

```
SHA-256
d709f370e52b57b4eb75f04e2b3422c4d41a05148cad8f81776d94a048fb70af
fdeeba79c3bb0348f9ac311909b56bf7e1891fe6f4e0793e82cc26abb181e8ed
c78310110ff5433fb24caf8dfd2728e6c54d71e9007bafaae71877d4b944afcb
```

```
BLAKE2s
033f324dc62f6c640253d171bfe7bc2e7592c73964773367732318b2622f40e5
caea936e64f327d6eaa9586753fecaaff566402512540111d5d8668aa92c92b4
eba706e62d21184a47e90053c05d40ba89240dc6c0f1b0c840a12c61fdd5af2d
```

```
BLAKE2b
a4da62dfc9863e10758f5e4300cd3e42ab92a16ccb5acbed8e9b712ba298409497265402157cee1ada0d22b98e02cc613ebbc616c4d48b2647a9e83bf8782027
1cfb90bb5d79cd7bbc6790f20119fdd12a4e1008793d7371e2a79cd573d5729504a8a92b4d6f914534193271a61a5b21495492fa4fc39db9bfe3275af7cabf4a
f7d7f8d74c2ebbe9bb80548866f55552000caccc03d3d27033a6b3061520402c6bc255508a59b383f415e067d372c96b654a75c9c5565e0ca63bd72c443469d7
```

##### Profiling

For a input file with 6400357 records, the execution times are:

    Hashed 6400357 email addresses in **17.73** seconds using sha256 to ...
    Hashed 6400357 email addresses in **14.47** seconds using blake2s to ...
    Hashed 6400357 email addresses in **16.14** seconds using blake2b to ...

##### Output File

By default, the output file name will be the name of the input file with the `.hashed` extension. To change that, use the `-o` or `--output` argument:

```
$ python3 hash.py --hash sha1 --output hashed.file test.csv 
Hashed 3 email addresses in 0.00 seconds using sha1 to /home/example/hashed.file
```

##### Verbosity

The script will output some execution information (line count, time taken and output file name) by default unless the `--silent` flag is specified.

```
$ python3 hash.py --hash sha1 --out hashed.file --silent test.csv 
The output file hashed.file exists and will be overwritten.
Proceed? (type yes or no): yes
```

If you pass a *bad* CSV file with the missing `email` column, the script will just quit. Please fix the CSV file and run the script again.
