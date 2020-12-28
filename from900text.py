# Convert 900 telecode to ACII - Andrew Herbert - 28/12/20

import argparse
import sys

newline = True

def convert(path):
    global newline
    with open(path, 'rb') as inFile:
        input  = (inFile.read())
        j = 0
        for i in range(len(input)):
            ch = input[i] & 127
            if ch == 10 or 32 <= ch <= 122:
                print(chr(ch), end='')
                newline = ch == 10

# Decode parameters
def getArgs():
    global inPath
    parser = argparse.ArgumentParser()
    parser.add_argument('-ptin',  help='paper tape punch file path')
    args = parser.parse_args()
    inPath = args.ptin if args.ptin!= None else '.punch'

# main program
sys.stdout.reconfigure(encoding='ASCII')
                            # force stdout to be ASCII encoding
getArgs()                   # get and decode command line arguments
convert(inPath)
if not newline:             # force new line at end of file if not present
    print()
