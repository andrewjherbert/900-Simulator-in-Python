# Convert 900 telecode to UTF-8 - Andrew Herbert - 15/07/20

import argparse

def convert(path):
    with open(path, 'rb') as inFile:
        input  = (inFile.read())
        j = 0
        for i in range(len(input)):
            ch = input[i] & 127
            if ch == 10 or 32 <= ch <= 122:
                print(chr(ch), end='')


# Decode parameters
def getArgs():
    global inPath
    parser = argparse.ArgumentParser()
    parser.add_argument('-ptin',  help='paper tape punch file path')
    args = parser.parse_args()
    inPath = args.ptin if args.ptin!= None else '.punch'

# main program
getArgs()                   # get and decode command line arguments
convert(inPath)
