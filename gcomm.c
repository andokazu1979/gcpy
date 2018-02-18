#define MPICH_SKIP_MPICXX 1
#define OMPI_SKIP_MPICXX  1
#include <mpi.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif
extern void sayhello(MPI_Comm);
extern void scatter(MPI_Comm, float*, int, float*, int, int);
#ifdef __cplusplus
}
#endif

void sayhello(MPI_Comm comm) {
  int size, rank;
  char pname[MPI_MAX_PROCESSOR_NAME]; int len;
  if (comm == MPI_COMM_NULL) {
    printf("You passed MPI_COMM_NULL !!!\n");
    return;
  }
  MPI_Comm_size(comm, &size);
  MPI_Comm_rank(comm, &rank);
  MPI_Get_processor_name(pname, &len);
  pname[len] = 0;
  printf("Hello, World! I am process %d of %d on %s.\n",
         rank, size, pname);
}

void scatter(MPI_Comm comm, float* sendbuf, int send_count, float* recvbuf, int recv_count, int root) {
  if (comm == MPI_COMM_NULL) {
    printf("You passed MPI_COMM_NULL !!!\n");
    return;
  }
  MPI_Scatter(sendbuf, recv_count, MPI_FLOAT, recvbuf, recv_count, MPI_FLOAT, root, comm);
}
