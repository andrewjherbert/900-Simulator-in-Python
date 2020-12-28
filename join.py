# Join 905 FORTRAN library tapes  - Andrew Herbert - 28/12/20

def Join():
    with open('905fortlib', 'wb') as outFile:
        with open('905fortlib1_iss4', 'rb') as lib1InFile:
            with open('905fortlib2_iss5', 'rb') as lib2InFile:
                outFile.write(lib1InFile.read()+lib2InFile.read())

# main program
Join()
