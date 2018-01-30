#! /bin/sh
#
# useage:
#  ./go.sh ${np} ${msize}
#
#  np:    number of processes
#  msize: matrix size

np=$1
msize=$2

mpirun -n ${np} python ./main.py ${msize}
