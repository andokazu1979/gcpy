#! /bin/sh
#
# useage:
#  ./go.sh ${np} ${gsize}
#
#  np:    number of processes
#  gsize: matrix size

np=$1
gsize=$2

mpirun -n ${np} python ./main.py ${gsize}
