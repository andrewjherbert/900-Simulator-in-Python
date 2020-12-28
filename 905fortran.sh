#!/bin/sh
rm .reader .punch .reverse .save .ptpasc
#echo loading Fortran
python3 900sim.py -ptin 905fortran_iss6
#echo convert input tape $1
python3 to900text.py src/905fortran/$1
#echo compile program
python3 900sim.py -jump 16 -ttyin src/905fortran/O0R
#echo compilation complete
mv .reader .save
#echo reverse output
python3 reverse.py
#echo load loader
python3 900sim.py -ptin loader_iss3
#echo load program binary
python3 900sim.py -ptin .reverse -jump 16 -ttyin src/905fortran/O20L
#echo load library
python3 900sim.py -ptin 905fortlib -jump 16 -ttyin src/905fortran/O3L
#echo complete load and run
python3 900sim.py -jump 16 -ttyin src/905fortran/MM -ptin .save
#echo check for punch output
touch .punch
python3 from900text.py >.ptpasc
if  [ ! -s .ptpasc ]
then
    echo No  punch output
else
    echo Punch output
    echo
    cat .ptpasc
fi



