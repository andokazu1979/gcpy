#! /bin/sh

CC=mpiicc
CXX=mpiicpc
FC=mpiifort
CFLAGS="-fast"
FFLAGS="-fast"

CC=${CC} CXX=${CXX} FC=${FC} CFLAGS=${CFLAGS} FFLAGS=${FFLAGS} cmake .
