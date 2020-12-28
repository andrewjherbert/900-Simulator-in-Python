#!/bin/sh
rm -f .reader .punch .ptputf .ptpasc
#echo loading Fortran
python3 900sim.py -ptin fort16klg_iss5
#echo convert input tape $1
python3 to900text.py src/903fortran/$1
#echo read program
python3 900sim.py -jump 8
if [ $? != 0 ]
then exit $?
fi
#echo signal program complete
python3 900sim.py -jump 10
echo
#echo run program
python3 900sim.py -jump 11
echo
echo
touch .punch
python3 from900text.py >.ptputf
iconv -c -f UTF-8 -t ASCII .ptputf >.ptpasc
if  [ ! -s .ptpasc ]
then
    echo No  punch output
else
    echo Punch output
    cat .ptpasc
fi




