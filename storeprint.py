# Display store file - Andrew Herbert - 04/07/2020

# Outputs .store in a legible format when .store is a store dump
# from 900sym.py

import sys
import argparse

def getArgs ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',  help='start address',  type=int,
                        default=8)
    parser.add_argument('-f', '--finish', help='finish address', type=int,
                        default=8180)
    args = parser.parse_args()
    return ('.store', args.start, args.finish)

toFraction = 2.0**-17

def printStoreFile (args):
    path, start, finish = args
    with open(path, 'r') as f:
        words = [ int(x) for x in f.read().split()]
    for i in range(start, min(finish+1, len(words))):
        n = words[i]
        if n >= 131072:
            n-= 262144
        inst = words[i]
        m = '/' if inst >= 131072 else ' '
        f = (inst >> 13) & 15
        pad = ' ' if f < 10 else ''
        a = inst & 8191
        fr = n * toFraction
        print('%5d: %+7d &%6o %+8.6f %s%s %d %4d' % (i, n, n, fr, pad, m, f, a))


printStoreFile(getArgs())
    
