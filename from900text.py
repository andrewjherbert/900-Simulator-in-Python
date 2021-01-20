# Convert 900 telecode to ASCII - Andrew Herbert - 06/01/21

import argparse
import sys

def Convert(inPath,outPath):
    newline = True
    with open(inPath, 'rb') as inFile:
        input=inFile.read()
        with open(outPath,'w',encoding='ASCII') as outFile:
            for i in range(len(input)):
                ch = input[i] & 127
                if ch == 10 or 32 <= ch <= 122:
                    print(chr(ch), end='',file=outFile)
                    newline = ch == 10
            if not newline: # force new line at end of file if not present
                print(file=outFile)

# Decode parameters
def GetArgs():
    global inPath, outPath
    parser = argparse.ArgumentParser()
    parser.add_argument('-ptin',  help='paper tape punch file path')
    parser.add_argument('-ascii', help='ascii output file path')
    args = parser.parse_args()
    inPath = args.ptin if args.ptin != None else '.punch'
    outPath = arg.ascii if args.ptin != None else '.ascii'

# main program

GetArgs()                   # get and decode command line arguments
Convert(inPath,outPath)
