CC = gcc
MPICC = mpicc
FC = gfortran
MPIFC = mpif90
LIBNAME_CALC_C = libgcalcc.so
LIBNAME_COMM_C = libgcommc.so
LIBNAME_CALC_F = libgcalcf.so
OPT = -O3
FLAGS = ${OPT} -shared -fPIC
CFLAGS = ${FLAGS}
FFLAGS = ${FLAGS}
LDFLAGS = 

.PHONY: default
default: build

.PHONY: build
build: ${LIBNAME_CALC_C} ${LIBNAME_COMM_C} ${LIBNAME_CALC_F}
${LIBNAME_CALC_C}: gcalc.c
	${CC} ${CFLAGS} ${LDFLAGS} -o $@ $<
${LIBNAME_COMM_C}: gcomm.c
	${MPICC} ${CFLAGS} ${LDFLAGS} -o $@ $<
${LIBNAME_CALC_F}: gcalc.f90
	${FC} ${FFLAGS} ${LDFLAGS} -o $@ $<

.PHONY: clean
clean:
	${RM} -rf ${LIBNAME_CALC_C} ${LIBNAME_CALC_F} ${LIBNAME_COMM_C} *.pyc __pycache__ *.lst
