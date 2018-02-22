#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif
extern void scaling(int, float*, int, int, int);
#ifdef __cplusplus
}
#endif

void scaling(int num, float* arr, int nx, int ny, int nz) {
    int i;
    int total = nx * ny * nz;
    for(i = 0; i < total; i++) {
        arr[i] = arr[i] * num;
    }
}
