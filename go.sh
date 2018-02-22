#! /bin/sh
#
# useage:
#  ./go.sh ${nx} ${ny} ${nz} ${px} ${py} ${pz}
#
#  nx: Grid size of x
#  ny: Grid size of y
#  nz: Grid size of z
#  px: Number of process for x-axis
#  py: Number of process for y-axis
#  pz: Number of process for z-axis

nx=$1
ny=$2
nz=$3
px=$4
py=$5
pz=$6
np=$(expr $px \* $py \* $pz)

mpirun -n ${np} python ./main.py ${nx} ${ny} ${nz} ${px} ${py} ${pz}
