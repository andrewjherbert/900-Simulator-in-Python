# Visualize binary paper tape file - Andrew Herbert - 04/07/2020

# Prints out a legible version of a binary paper tape

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
        ch = buf[i]
        print('%3d =' % ch, end = '')
        st = ''
        for bit in [128, 32, 16, 8, -1, 4, 2, 1]:
            if bit == -1:
                st += '.'
            elif ch&bit != 0:
                st += '0'
            else:
                st += ' '
        print(st)
            

printFile(getArgs())
    
