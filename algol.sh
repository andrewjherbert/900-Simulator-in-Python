#!/bin/sh
rm .reader
echo loading Algol
python3 900sim.py -ptin alg16klg_masd
echo convert input tape
python3 to900text.py src/algol/$1
echo run translator
python3 900sim.py -jump 8
echo
echo
echo run interpreter
rm .punch*
python3 900sim.py -jump 10
echo display punch output
python3 from900text.py
echo




