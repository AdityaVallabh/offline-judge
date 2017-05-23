#!/usr/bin/python3

import sys
from os.path import exists as path_exists
from os import remove
from filecmp import cmp as diff
from subprocess import run, PIPE, CalledProcessError, TimeoutExpired, call, DEVNULL
from time import time

OUTPUT_FILE = '.OUTPUT_TEMP'
TIMEOUT = 2

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
                for letter in range(0,len(word),2):
                    dec.write(' '.join([word if(word == ' ') else chr(int(word[letter:letter+2], 8))]))
                dec.write(' ')
            dec.write('\n')

def run_program(exe, TEST_CASES):
    i = 0
    for test_case in TEST_CASES:
        decode(test_case[0])
        decoded_file = '.' + test_case[0][:-3] + 'dec'
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
         "failed" if (not diff(test_case[1], OUTPUT_FILE) or failed)
         else "passed",
         sep='\t')
        clean_up(decoded_file)

def main():
    if (len(sys.argv) < 4):
        return
    filename = sys.argv[1]
    datafiles = sys.argv[2:]
    iofiles = []
    for f in datafiles:
        if (not path_exists(f)):
            print(f, "does not exist")
            return
    i = 0
    while i < int(len(datafiles) / 2):
        iofiles.append((datafiles[i], datafiles[int(len(datafiles) / 2) + i]))
        i += 1
    
    check_program(filename)

    if path_exists(filename[:-2]):
        print("# Test case\tTime taken\tPassed")
        print("#--------------------------------------")
        run_program(filename[:-2], iofiles)
        clean_up(filename[:-2])

if __name__ == "__main__":
    main()
