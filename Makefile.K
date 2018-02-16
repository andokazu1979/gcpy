CC = fcc
FC = frt
LIBNAME_C = libgcalcc.so
LIBNAME_F = libgcalcf.so
OPT = -Kfast
INCLUDE = -I/opt/klocal/Python-3.5.4-fujitsu/include/python3.5m -I/opt/klocal/Python-3.5.4-fujitsu/lib/python3.5/site-packages/mpi4py/include
FLAGS = ${OPT} -shared -KPIC ${INCLUDE}
CFLAGS = ${FLAGS} -Nlst=t
FFLAGS = ${FLAGS} -Qt
LDFLAGS = -L/opt/klocal/Python-3.5.4-fujitsu/lib -ldl -lutil -lm -lpython3.5m

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
