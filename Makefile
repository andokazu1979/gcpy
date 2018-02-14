.PHONY: default
default: build

PYTHON = python

CC = gcc
LIBNAME = libgcalc.so
.PHONY: build
build: ${LIBNAME}
${LIBNAME}: gcalc.c
	${CC} -O3 -shared -fPIC -o $@ $<

.PHONY: clean
clean:
	${RM} -r ${LIBNAME} *.pyc __pycache__
