# Convert utf file to 900 telecode - Andrew Herbert - 05/07/20

import argparse

inPath = ''

def addParity (code):
    p = 0
    c = code
    while c != 0:
        if c & 1 > 0:
            p+=1
        c>>=1
    if p & 1 > 0:
        return code | 128 # odd parity, add parity digit
    else:
        return code       # even parity

def convert(path):
    with open('.reader', 'wb') as outFile, open(path, 'r', encoding='utf-8-sig') as inFile:
        input = (inFile.read())
        input = input.replace('<! HALT !>', chr(20))
        output = bytearray(len(input))
        for i in range(len(input)):
            output[i] = addParity(ord(input[i]))
        outFile.write(output)

# Decode parameters
def getArgs():
    global inPath
    parser = argparse.ArgumentParser()
    parser.add_argument('input',  help='paper tape input file path')
    args = parser.parse_args()
    inPath = args.input

# main program
getArgs()                   # get and decode command line arguments
convert(inPath)
