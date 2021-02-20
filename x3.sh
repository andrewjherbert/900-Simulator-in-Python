#!/bin/sh
echo Run X3 Functional test
python3 900sim.py -ptin x3_iss4
echo X3 loaded
rm -f .punch
time python3 900sim.py -jump 8 -limit 6823740
python3 tapevisual.py .punch
