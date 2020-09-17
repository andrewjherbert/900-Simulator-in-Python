#!/bin/sh
echo Run X3 Functional test
python3 900sim.py -ptin x3_iss4
echo X3 loaded
python3 900sim.py -jump 8 -limit 10000000

