#!/bin/sh
rm -rf .reader .punch .reverse .save .ascii
#echo
echo
echo "***"
echo "*** Loading 905 FORTRAN compiler and reading source code tape."
echo "*** Outputs a relocatable binary tape and halts."
echo "***"
python3 900sim.py -ptin 905fortran_iss6
#echo convert input tape $1
python3 to900text.py src/905fortran/$1
#echo compile program
python3 900sim.py -jump 16 -ttyin src/905fortran/O0R
echo
echo "***"
echo "*** Compilation complete - now loading binary using \"900 LINKER\"."
echo "***"
# save paper tape in case contains data
mv .reader .save
#echo reverse output
python3 reverse.py
#echo load loader
python3 900sim.py -ptin loader_iss3
#echo load program binary
python3 900sim.py -ptin .reverse -jump 16 -ttyin src/905fortran/O20L
echo
echo "***"
echo "*** Now loading FORTRAN library routines."
echo "***"
python3 900sim.py -ptin 905fortlib -jump 16 -ttyin src/905fortran/O3L
#echo complete load and run
echo
echo "***"
echo "*** Now running compiled program"
echo "***"
# clear punch
rm .punch
touch .punch
python3 900sim.py -jump 16 -ttyin src/905fortran/MM -ptin .save
echo
echo "***"
echo "*** Program run complete."
echo "***"
#echo check for punch output
touch .ascii
python3 from900text.py
echo
echo "***"
if  [ ! -s .ascii ]
then
    echo ***" No punch output ***"
    echo "***"
else
    echo "*** Punch output ***"
    echo "***"
    cat .ascii
fi
echo



