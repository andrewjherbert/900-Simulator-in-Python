# Elliott 903 simulator - Andrew Herbert - 02/09/2020

# Simulator for Elliott 903 / 920B
# Does not implement 'undefined' effects
# Has simplified handling of priority levels and initial orders
# Teletype input is not implemented.

# At beginning reads in contents of store from file .store if available,
# at end, dumps out contents of store to .store, unless catastrophic errors.
# This is to simulate retention of data in core store between entry points.
# There is a companion program "storeprint.py" which can be used to obtain
# an interpreted listing of the store.

# By default reads input from file .reader unless overriden by -ptin option
# on command line.  At end writes any unconsumed paper tape input to .reader,
# unless catastrophic errors, overwriting existing contents.  This is to
# simulate leaving a tape in the reader between successive entry points.
# The input file should be raw bytes representing eight bit paper tape
# codes, either binary of one of the Elliott telecodes.  There is a companion
# program "to900text.py" which converts a UTF-8 character file to it's equivalent
# in Elliott 900 telecode.

# By default paper tape output is send to file .punch, unless overridden by
# -ptout option on command line.  There is a companion program "from900text.py"
# which converts a file containing 900 telecode output to it's UTF-8 equivalent.

# By default the simulator jumps to 8181 to start execution, unless overriden by
# -jump option on command line.

# A limit on maximum number of instructions to be executed can be set using
# the -limit command line option.

# A trace in file .trace will be written if -trace command line option is
# present.  There is a companion program "traceprint.py" that produces am
# interpreted listing of the trace.

import sys
import os.path
import argparse
import time

# Error handling

def failure (s):
    print ('***Error - ', s)
    endTracing () # close tracing if any to ensure wriiten to file
    sys.exit(-1)

# Useful constants for 18 and 13 bit arithmetic
bit19    = 1<<18    # arithmetic is 2's complement 18 bits
mask18   = 0o777777
bit18    = 1<<17
mask16   = 0o177777 # absolute addresses are 16 bits
addrMask = 8191     # offset within module in an absolute address
modMask  = 0o160000 # module number in an absolute address

# Function to convert 18 bit values to numbers
def normal (n):
    if n >= bit18:
        return n - bit19
    else:
        return n

# Execution tracing
traceDefault = '.trace'
tracePath    = traceDefault
traceFile    = None

def startTracing ():
    global traceFile
    try:
        traceFile = open(tracePath, 'w')
    except:
        failure('cannot open trace file ' + tracePath)

def endTracing ():
    if not (traceFile is None):
        traceFile.close()

def trace (s):
    if not (traceFile == None):
        traceFile.write(s+'\n')

# 16K store
maxStore = 16*1024
store = [0 for addr in range(maxStore)]

def clearStore ():
    for word in store:
        word = 0

# readStoreFromFile, writeStoreToFile -- functions to dump out store
# to a file as a sequence of integers, to enable store to be preserved
# between runs of the program

storePath = '.store'

def readStoreFromFile ():
    # if path exists, read in contents of store as integers
    if not os.path.exists(storePath):
        clearStore()
    else:
        with open (storePath) as f:
            words = [int(x) for x in f.read().split()]
        store[:len(words)] = words

def writeStoreToFile ():
    with open(storePath, mode='w') as f:
        for i in range(maxStore):
         print('%7d' % store[i], file=f, end=('\n' if i % 10 == 9 else ''))

# Paper tape input/output
ptrDefault = '.reader'
ptrPath    = ptrDefault # can be overridden by command option -ptin
ptrBuf     = None
ptrIdx     = 0

ptpDefault = '.punch'
ptpPath    = ptpDefault # can be overridden by command line option -ptout
ptpFile    = None

# Save any remaining paper tape to simulate leaving tape in reader between runs
def closeReader ():
    if not (ptrBuf is None):
        try:
            with open(ptrDefault, 'wb') as f:
                f.write(ptrBuf[ptrIdx:])
        except: failure('cannot save remaining paper tape to ' + ptrDefault)

# Close paper tape punch to ensure output to file
def closePunch ():
    if not (ptpFile is None):
        ptpFile.close()

# Read input paper tape
def readTape ():
    global ptrBuf, ptrIdx
    if ptrBuf is None:
        try:
            with open(ptrPath, 'rb') as f: # open input file on first 15 2048
                ptrBuf = f.read()
        except: failure('cannot open input file ' + ptrPath)
    if ptrIdx >= len(ptrBuf):
        msg = 'run off end of input tape'
        trace(msg)
        endTracing()
        writeStoreToFile() # preserve store in this case to allow resume
        failure(msg)
    code = ptrBuf[ptrIdx]
    if code < 0 | code > 128:
        failure('invalid code in paper tape input - %d' & code)
    ptrIdx+=1
    if not (traceFile is None):
        trace('read code %3d' % code)
    return code

# Output to paper tape punch
def punchTape (code):
    global   ptpFile
    if ptpFile is None:
        try:
            ptpFile = open(ptpPath, 'wb') # open output file on first 15 6144
        except: failure('cannot open paper tape output file ' + ptpPath)
    ptpFile.write(bytes([code]))

def readTTY ():
    failure('teletype input not implemented')

def writeTTY (code):
    ch = code & 127
    if ch == 10 or 32 <= ch <= 122:
        sys.stdout.write(chr(ch))

# Internal machine state

# Accumulator and extension (Q register)
aReg = 0
qReg = 0

# Interrupt level - will be either 1 or 4. real machine has 1, 2, 3, 4
level = 1

# Addresses of b register and sequence control register depend on level
sLevel1 = 0
bLevel1 = 1
sLevel4 = 6
bLevel4 = 7

scr  = sLevel1
bReg = bLevel1

def makeIns (m, f, n):
    # create an instruction from m, f and n fields
    return (((m << 4) + f) << 13) + n

# Simulate initial orders by writing them to store
def establishInitialInstructions ():
    store[8180] = (-3 & mask18)
    store[8181] = makeIns(0,  0, 8180)
    store[8182] = makeIns(0,  4, 8189)
    store[8183] = makeIns(0, 15, 2048)
    store[8184] = makeIns(0,  9, 8186)
    store[8185] = makeIns(0,  8, 8183)
    store[8186] = makeIns(0, 15, 2048)
    store[8187] = makeIns(1,  5, 8180)
    store[8188] = makeIns(0, 10,    1)
    store[8189] = makeIns(0,  4,    1)
    store[8190] = makeIns(0,  9, 8182)
    store[8191] = makeIns(0,  8, 8177)

# Instructions, operate on aReg, qReg and store.
#SCR and B register are accessed via the store rather than memoed.

#  0 Load B
def loadB(addr):
    global qReg
    qReg = store[addr]
    store[bReg] = qReg

#  1 Add
def add (addr):
    global aReg
    aReg = (aReg + store[addr]) & mask18

#  2 Negate and Add
def negAdd (addr):
    global aReg, qReg
    aReg = (store[addr] - aReg) & mask18
    qReg = addr

#  3 Store Q
def storeQ (addr):
    store[addr] = qReg >> 1

#  4 Load A
def loadA (addr):
    global aReg
    aReg = store[addr]

#  5 Store A

def storeALevel1 (addr):
    global store
    if 8180 <= addr <= 8191: # need this for FORTRAN to work
        trace('write to initial instructions ignored')
        return
    store[addr] = aReg

def storeALevel4 (addr):
    global store
    store[addr] = aReg

#  6 Collate
def collate (addr):
    global aReg
    aReg &= store[addr]

#  7 Jump if zero
def jumpZ (addr):
    global store
    if aReg == 0:
        store[scr] = addr

#  8 Jump unconditional
def jump (addr):
    global store
    store[scr] = addr

#  9 Jump negative
def jumpN (addr):
    global store
    if aReg >= bit18:
        store[scr] = addr

# 10 Count in store
def count (addr):
    global store
    store[addr] = (store[addr] + 1) & mask18

# 11 Store S
def storeS (addr):
    global qReg, store
    s = store[scr]
    qReg = s & modMask
    store[addr] = s & addrMask

# def aqShiftR ():
#     global aReg, qReg
#     qReg = (qReg >> 1) | (bit18 if aReg & 1 == 1 else 0)
#     aReg = (aReg >> 1) | (bit18 if aReg >= bit18 else 0)
#
#
# def aqShiftL ():
#     global aReg, qReg
#     aReg = ((aReg << 1) | (1 if qReg >= bit18 else 0)) & mask18
#     qReg = (qReg << 1) & mask18

# 12 Multiply - n.b. depends on Python multi-length arithmetic to handle 36 bit AQ
def multiply (addr):
    global aReg, qReg
    a = normal(aReg)
    intprod = (a * normal(store[addr]))
    qReg = (intprod <<  1) & mask18
    # set bit 1 of Q to make X3 happy - spec says "undefined".
    if a<0:
        qReg = qReg | 1
    aReg = (intprod >> 17) & mask18

# 12 Multiply: simulate microcode
# def multiply (addr):
#     global aReg, qReg
#     m = store[addr]
#     for processCounter in range(1, 19):
#         if processCounter == 1:
#             qReg  = aReg
#             aReg  = 0
#             xbits = qReg << 1
#         else:
#             xbits = qReg
#             aqShiftR()
#         xbits &= 3
#         if xbits == 1:
#             aReg = (aReg + m) & mask18
#         elif xbits == 2:
#             aReg = (aReg - m) & mask18
#         if m == bit18 & aReg != 0:
#             correct for using 18 bits where hardware uses 19 bits
#             aReg = bit19 - aReg

# 13 Divide
def divide(addr):
	global aReg, qReg
	aq = (normal(aReg) << 18) | qReg
	m  = normal(store[addr])
	intquot = ((aq // m) >> 1) & mask18
	aReg = intquot | 1
	qReg = intquot & 0o777776

# 13 Divide: simulate microcode
# def divideMC (addr):
#     global aReg, qReg
#     m = store[addr]
#     qReg = qReg & 0o777776
#     xbits = aReg
#     for processCounter in range (1, 19):
#         if (xbits >= bit18) == (m >= bit18):
#             qReg += 1
#             aReg = (aReg - m) & mask18
#         else:
#             aReg = (aReg + m) & mask18
#         xbits = aReg
#         aqShiftL()
#     aReg = qReg + 1

# 14 Shift, etc - n.b. depends on Python multi-length arithmetic to handle 36 bit AQ
def shift (addr):
    global aReg, qReg
    places = addr & addrMask
    aq = (aReg << 18) | qReg
    if places <= 2047:
        aq = aq << places
        aReg = (aq >> 18) & mask18
        qReg = aq & mask18
    elif places >= 6144:
        places = 8192-places
        aq = ((normal(aReg) << 18) | qReg) >> places
        aReg = (aq >> 18) & mask18
        qReg = aq & mask18
    else:
        failure('unsupported i/o 14 %4d' & places)

# 15 Input/output etc
def inOut (addr):
    global aReg, level, scr, bReg, putStore, functionDict
    opAddr = addr & addrMask
    if opAddr == 7168:
        # Level terminate
        level = 4
        scr = sLevel4
        bReg = bLevel4
        functionDict[5] = storeALevel4
    elif opAddr == 2048:
        byte = readTape()
        if byte != 0:
            monitor = True
        aReg = ((aReg << 7) | byte) & mask18
    elif opAddr == 6144:
        punchTape(aReg & 255)
    elif opAddr == 6148:
        writeTTY(aReg & 255)
    else:
        failure('Unsupported i/o 15 %4d' % opAddr)

# Set up function code mapping to functions
functionDict = {  0: loadB,     1: add,           2: negAdd,   3: storeQ,
                  4: loadA,     5: storeALevel1,  6: collate,  7: jumpZ,
                  8: jump,      9: jumpN,        10: count,   11: storeS,
                 12: multiply, 13: divide,       14: shift,   15: inOut}

# Instruction fetch and decode

lastS = 0  # detect a dynmaic stop if SCR isn't changed

limit = 200000000 # about one hundred hours of computation

def endRun (s):
    closeReader()      # save remaining paper tape
    closePunch()       # close paper tape output file
    endTracing()       # save trace output, if any
    writeStoreToFile() # save store contents
    sys.exit(s)

def decode ():
    global lastS, limit, scr
    # instruction fetch, decode and execute loop
    while limit > 0: # break out on a dynamic stop
        limit -= 1
        # Update SCR
        lastS = store[scr]
        store[scr] += 1
        # Fetch instruction and break out fields
        instruction = store[lastS]
        f = (instruction >> 13) & 15
        a = (instruction & addrMask) | (lastS & modMask)
        m = ((a + store[bReg]) if instruction >= bit18 else a) & mask16
        trace('%d %d %d %d %d' % (lastS, instruction, aReg, qReg, store[bReg]))
        functionDict[f](m)
        if store[scr] == lastS:
            msg = 'Dynamic stop at %d' % store[scr]
            trace(msg)
            #print('\n', msg, sep='')
            return lastS
    msg = 'execution limit reached'
    trace(msg)
    writeStoreToFile()
    failure(msg)

jumpAddr = 8181 # default to running initial orders

# Decode parameters
def getArgs():
    global ptrPath, ptpPath, jumpAddr, limit
    parser = argparse.ArgumentParser()
    parser.add_argument('-ptin',  help='paper tape input file path',
                        default='')
    parser.add_argument('-ptout', help='paper tape output file path',
                        default='')
    parser.add_argument('-jump', help='start address', default='')
    parser.add_argument('-trace',help='turn on tracing to .trace',
                        action="store_true")
    parser.add_argument('-limit', help='instruction execution limit',
                        type=int)
    args = parser.parse_args()
    if args.ptin != '':
        ptrPath = args.ptin
    if args.ptout != '':
        ptpPath = args.ptout
    if args.jump != '':
        addr = int(args.jump)
        if 8 <= addr <= 8181:
            jumpAddr = addr
        else:
            failure('start address must be in range 8-8181')
    if args.trace:
        startTracing()
    if args.limit:
        if args.limit < 1:
            failure('nonsensical limit - %d', args.limit)
        else:
            limit = args.limit

# main program
getArgs()                        # get and decode command line arguments
readStoreFromFile()              # reload store from previous run, if available
if jumpAddr == 8181:
    establishInitialInstructions ()  # set up initial instructions
store[scr] = jumpAddr                # initialise sequence control register
#startTime = time.time()
res = decode()                   # run instruction fetch decode loop
#stopTime = time.time()
#print('Execution time', stopTime-startTime, 'secs')
endRun (res)








