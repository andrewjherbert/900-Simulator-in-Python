# Print binary paper tape file - Andrew Herbert - 04/07/2020

# Prints a binary paper tape file as a sequence of decimal numbers
# 10 per line.

import sys
import argparse

def getArgs ():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    return args.input

def printFile (path):
    with open(path, 'rb') as f:
        buf = f.read()
    for i in range(len(buf)):
        print('%4d' % buf[i], end='')
        if i%10 == 9:
            print()

printFile(getArgs())
    
