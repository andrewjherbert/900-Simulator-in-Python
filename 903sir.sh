#!/bin/sh
rm -f .reader .punch .ascii .save
#echo loading SIR assembler
python3 900sim.py -ptin "sir(iss6)(5500)"
#echo convert input tape $1
python3 to900text.py src/903sir/$1.txt
#echo read in program
python3 900sim.py -jump 8
if [ $? != 0 ]
then exit $?
fi
#echo run program
python3 900sim.py -jump 32
#check for punch output
touch .punch
python3 from900text.py
echo
if  [ ! -s .ascii ]
then
    echo "*** No punch output ***"
else
    echo "*** Punch output ***"
    cat .ascii
fi




