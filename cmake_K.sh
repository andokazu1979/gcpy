#! /bin/sh

CC=mpifccpx
CXX=mpiFCCpx
FC=mpifrtpx
CFLAGS="-Kfast -Nlst=t"
FFLAGS="-Kfast -Qt"

CC=${CC} CXX=${CXX} FC=${FC} CFLAGS=${CFLAGS} FFLAGS=${FFLAGS} cmake .
