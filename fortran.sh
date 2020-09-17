#!/bin/sh
rm .reader
echo loading Fortran
python3 900sim.py -ptin fort16klg_iss5
echo convert input tape $1
python3 to900text.py src/fortran/$1
echo read program
python3 900sim.py -jump 8
echo signal program complete
python3 900sim.py -jump 10
echo
echo run program
rm .punch*
python3 900sim.py -jump 11
echo
echo display punch output
python3 from900text.py
echo
echo




