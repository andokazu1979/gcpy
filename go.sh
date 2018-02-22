#! /bin/sh
#
# useage:
#  ./go.sh ${np} ${gsize}
#
#  np:    number of processes
#  gsize: matrix size

np=$1
nx=$2
ny=$3
nz=$4
px=$5
py=$6
pz=$7

mpirun -n ${np} python ./main.py ${nx} ${ny} ${nz} ${px} ${py} ${pz}
