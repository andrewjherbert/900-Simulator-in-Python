#!/bin/sh
rm -f .reader .punch .ascii
#echo loading Algol
python3 900sim.py -ptin alg16klg_masd
#echo convert input tape
python3 to900text.py src/algol/$1
#echo run translator
python3 900sim.py -jump 8
if [ $? != 0 ]
then exit $?
fi
echo 
echo
#echo run interpreter
python3 900sim.py -jump 10
touch .punch
python3 from900text.py
if  [ ! -s .ascii ]
then
    echo "*** No punch output ***"
    echo
else
    echo "*** Punch output ***"
    echo
    cat .ascii
fi






