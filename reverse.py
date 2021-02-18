# Reverse .punch binary file to .reverse  - Andrew Herbert - 28/12/20

def Reverse(path):
    with open('.reverse', 'wb') as outFile, open(path, 'rb') as inFile:
        input = (inFile.read())
        output = input[::-1]
        outFile.write(output)

# main program
Reverse('.punch')
