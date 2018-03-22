cmake_minimum_required (VERSION 2.8)

project(gcalc)

enable_language (Fortran)

find_package(MPI REQUIRED)
include_directories(SYSTEM ${MPI_INCLUDE_PATH})

ADD_LIBRARY(gcalcc SHARED gcalc.c)
ADD_LIBRARY(gcalcf SHARED gcalc.f90)
ADD_LIBRARY(gcomm SHARED gcomm.c)
