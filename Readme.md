##**Offline-Lab-Judge**

This is the initial prototype of the offline-judge.

** Format: "$ python3 check.py ./file.c input1.enc input2.enc output1 output2" **

###How it works?
* Accepts the C file along with a variable number of input and output files
* Compiles the given C file
* Decodes the input file encoded with _dummy_ algorithm
* Tests the binary against the various decrypted input files
* Compares the outfiles and generates the result

###To-Do:
* ~~Encrypt the input files~~
* Compare hashes of the output files
* Evaluate multiple codes
* Automatically fetch input files and output hashes
* Establish a connection and post scores to a server
