# 900-Simulator-in-Python


A simple simulator in Python for the Elliott 900 range of minicomputers

This repository consists of a simulator for the Elliott 900 series of minicomputers
written in Python, along with supporting utilities.

A faster simulator, written in C, and with enhanced diagnostics is available at:

    https://github.com/andrewjherbert/900-Simulator-in-C

900sim.py is the simulator.

binprint.py converts a binary file (sequence of raw bytes) into a sequence of tabulated
decimal numbers.  This can be useful for interpreting binary Elliott input files.

from900text.py is a utility program to convert Elliott 900 paper tape and teleprinter
code output to equivalent ASCII.

storeprint.py is a utility to print out a dump from a 900sim.py ".store" file.

tapevisual.py prints out a legible rendition of a binary file resembling physical paper
tape.

to900text.py converts a file containing ASCII characters to its equivalent in the Elliott
900 paper tape and teleprinter code.

traceprint.py prints out in human readable for a ".trace" file from 900sim.py.

900sim.py is the principal program to use.  It reads a dump of the machine store from a
file ".store" if present.  paper tape input is read from the file ".reader" which should
be a sequence of bytes binary file containing either an image of an Elliott paper tape or
the result of translating an ASCII file to Elliott 900 Telecode using to990text.py.
900sim writes all teleprinter output to stdout.  Teleprinter input is read from the file
".ttyin".   Any paper tape punch output is written as a sequence of bytes to the file
".punch".  If the output was in Elliott 900 Telecode it can be converted to ASCII using f
rom900text.py.  If it is is binary output, binprint.py or tape visual.py may be useful to
interpret the content.

At the end of a run of 900sim.py .reader is updated to contain any unconsumed input and
.store is updated with the new contents of the store.  If tracing is request a trace file
will be written to the file ".trace" for interpretation by traceprint.py.

There are scripts algol.sh, 903fortran.sh 905fortran.sh to run example programs
which can be found in src/algol (Elliott Algol60), src/903fortran (Elliott FORTRAN
II), src/905fortran (Elliott FORTRAN IV).

There are also .dox / .pdf files containing a short "manual" for each of langauges

The script x3.sh runs the Elliott 900 functional test program X3.
