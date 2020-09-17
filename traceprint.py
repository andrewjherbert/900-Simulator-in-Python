# 900sim trace analysis - Andrew Herbert - 04/07/2020

def normal (n):
    return n - 262144 if n >= 131072 else n

def decodeTrace (line):
    items = []
    for i in line.split():
        items.append(int(i))
    addr = items[0]
    inst = items[1]
    m    = '/' if inst >= 131072 else ' '
    f    = (inst >> 13) & 15
    a    = inst & 8191
    pad  = (' ' if f < 10 else '')
    aReg = normal(items[2])
    qReg = normal(items[3])
    bReg = normal(items[4])
    print('%6d: %s%s%d %4d A=%8d Q=%8d B=%8d' % (addr, pad, m, f, a,
                                                 aReg, qReg, bReg))
    
def decodeLine (line):
    if len(line) < 0:
        return()
    elif (line[0]).isdigit():
        decodeTrace(line)
    else:
        print(line)
        
def decodeFile (file):
    for line in file:
        decodeLine(line)
        
with open('.trace') as file:
    decodeFile (file)
