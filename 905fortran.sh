#!/bin/sh
rm .reader
echo loading Fortran
python3 900sim.py -ptin 905fortran_iss6
echo convert input tape $1
python3 to900text.py src/905fortran/$1
echo compile program
python3 900sim.py -jump 16 -ttyin src/905fortran/O0R
echo compilation complete




