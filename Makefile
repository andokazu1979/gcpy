CC = gcc
FC = gfortran
LIBNAME_C = libgcalcc.so
LIBNAME_F = libgcalcf.so
OPT = -O3
FLAGS = ${OPT} -shared -fPIC ${INCLUDE}
CFLAGS = ${FLAGS}
FFLAGS = ${FLAGS}
LDFLAGS = 

.PHONY: default
default: build

.PHONY: build
build: ${LIBNAME_C} ${LIBNAME_F}
${LIBNAME_C}: gcalc.c
	${CC} ${CFLAGS} ${LDFLAGS} -o $@ $<
${LIBNAME_F}: gcalc.f90
	${FC} ${FFLAGS} ${LDFLAGS} -o $@ $<

.PHONY: clean
clean:
	${RM} -rf ${LIBNAME_C} ${LIBNAME_F} *.pyc __pycache__ *.lst
