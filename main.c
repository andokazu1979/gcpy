#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"

int main(int argc, char *argv[]) {
    int i;
    int rank;
    int nproc;
    int n = 12;
    float* arr1 = NULL;
    float* arr2 = NULL;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    printf("myrnak = %d(of %d)\n", rank, nproc);

    if (rank == 0) {
        arr1 = (float*)malloc(sizeof(float) * n);
        for (i = 0; i < n; i++) {
            arr1[i] = (float)i;
            printf("arr1: %d %f\n", i, arr1[i]);
        }
    }
    arr2 = (float*)malloc(sizeof(float) * n / nproc);

    MPI_Scatter(arr1, n / nproc, MPI_FLOAT, arr2, n / nproc, MPI_FLOAT, 0, MPI_COMM_WORLD);

    for (i = 0; i < n / nproc; i++) {
        printf("myrank = %d arr: %f\n", rank, arr2[i]);
    }

    MPI_Finalize();
    return 0;
}
