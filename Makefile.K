CC = fcc
MPICC = mpifcc
FC = frt
MPIFC = mpifrt
LIBNAME_CALC_C = libgcalcc.so
LIBNAME_COMM_C = libgcommc.so
LIBNAME_CALC_F = libgcalcf.so
OPT = -Kfast
INCLUDE = -I/opt/klocal/Python-3.5.4-fujitsu/include/python3.5m -I/opt/klocal/Python-3.5.4-fujitsu/lib/python3.5/site-packages/mpi4py/include
FLAGS = ${OPT} -shared -KPIC ${INCLUDE}
CFLAGS = ${FLAGS} -Nlst=t
FFLAGS = ${FLAGS} -Qt
LDFLAGS = -L/opt/klocal/Python-3.5.4-fujitsu/lib -ldl -lutil -lm -lpython3.5m

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
