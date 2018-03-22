#! /bin/sh

CC=mpicc
CXX=mpicxx
FC=mpif90
CFLAGS="-O3"
FFLAGS="-O3"

CC=${CC} CXX=${CXX} FC=${FC} CFLAGS=${CFLAGS} FFLAGS=${FFLAGS} cmake .
