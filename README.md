# Bloom Filter Project

## main.py

### Dependencies
This file is the application. There is one external dependency, which is `bitarray`. To install this dependency, use the following command: 

```
pip install bitarray
```

When attempting to install this dependency on the Engineering Servers, the command is slightly different.

```
pip3 install bitarray --user
```
### Folder Structure

There are three important files for this project: `main.py`, `dictionary.txt`, and `rockyou.txt`. Both `.txt` files are in a files folder. Here is the folder structure:

```
files/
  - dictionary.txt
  - rockyou.txt
main.py
```

### Files

This project is implemented to run with two files: rockyou.txt and dictionary.txt.

#### rockyou.txt

This file is used to create the bloom filter. This is the list of words that we will use as our base. There are a total of 14,344,392 lines in this file.

#### dictionary.txt

This file contains the words we would like to test against our bloom filter. There are a total of 623,518 words in this dictionary.

#### main.py

This file is the main application. To run this file use the command: 

```
python3 main.py
```

This program will serialize the bloom filters for faster processing after the initial run. To run less than all of the filters, modify the `filter_params` list and remove one or more filters, and re-run the application.