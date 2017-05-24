#!/usr/bin/python3

import sys
import hashlib
from os.path import exists as path_exists
from os import remove
from filecmp import cmp as diff
from subprocess import run, PIPE, CalledProcessError, TimeoutExpired, call, DEVNULL
from time import time

OUTPUT_FILE = '.OUTPUT_TEMP'
TIMEOUT = 2

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def clean_up(filename):
    if path_exists(OUTPUT_FILE):
        remove(OUTPUT_FILE)
    if path_exists(filename):
        remove(filename)

def check_program(filename):
    failed = call(["gcc",filename, "-o", filename[:-2]], stdout=DEVNULL, stderr=DEVNULL, timeout=TIMEOUT)
    if failed: 
        print("Compilation Error")

def decode(f):
    dec = open('.' + f[:-4]+".dec","w")
    with open(f) as fi:
        for line in fi:
            for word in line.split():
                for letter in range(0,len(word),3):
                    dec.write(' '.join([word if(word == ' ') else chr(int(word[letter:letter+3], 8))]))
                dec.write(' ')
            dec.write('\n')

def run_program(exe, TEST_CASES):
    i = 0
    const = len(TEST_CASES)
    decode('hashes.enc')
    hashes = open('.hashes.dec').readlines()
    for test_case in TEST_CASES:
        if md5(test_case) != hashes[i][:-2]:
            return -1
        decode(test_case)
        decoded_file = '.' + test_case[:-3] + 'dec'
        ipf = open(decoded_file)	
        opf = open(OUTPUT_FILE, 'w')
        TLE = False
        failed = False
        start_time = time()
        try:
            run(exe, stdin=ipf, stdout=opf, stderr=PIPE, timeout=TIMEOUT,
                check=True)
        except TimeoutExpired:
            TLE = True
            pass
        except CalledProcessError as e:
            failed = True
        finally:
            ipf.close()
            opf.close()
        end_time = time()
        i += 1

        print(i,
         (end_time - start_time) if not TLE else "\tTLE\t",
         "failed" if (not md5(OUTPUT_FILE) == hashes[i+const-1][:-2] or failed)
         else "passed",
         sep='\t')
        clean_up(decoded_file)

def main():
    if (len(sys.argv) < 3):
        return
    filename = sys.argv[1]
    datafiles = sys.argv[2:]
    iofiles = []
    for f in datafiles:
        if (not path_exists(f)):
            print(f, "does not exist")
            return
    
    check_program(filename)

    if path_exists(filename[:-2]):
        print("# Test case\tTime taken\tPassed")
        print("#--------------------------------------")
        run_program(filename[:-2], datafiles)
        clean_up(".hashes.dec")
        clean_up(filename[:-2])

if __name__ == "__main__":
    main()
