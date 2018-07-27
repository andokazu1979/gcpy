#! /bin/sh

CC=mpiicc
CXX=mpiicpc
FC=mpiifort
CFLAGS="-O3"
FFLAGS="-O3"

CC=${CC} CXX=${CXX} FC=${FC} CFLAGS=${CFLAGS} FFLAGS=${FFLAGS} cmake .
