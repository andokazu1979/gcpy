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
nt=$4
px=$5
py=$6
pz=$7
pt=$8
input=$9
output=$10
np=$(expr $px \* $py \* $pz \* $pt)

mpirun -n ${np} python ./main.py ${nx} ${ny} ${nz} ${nt} ${px} ${py} ${pz} ${pt} ${input} ${output}
