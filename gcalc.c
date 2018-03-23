#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif
extern void scaling(int, float*, int, int, int, int);
extern void subst(float*, float*, int);
#ifdef __cplusplus
}
#endif

void scaling(int num, float* arr, int nx, int ny, int nz, int nt) {
    int i;
    int total = nx * ny * nz * nt;
    for(i = 0; i < total; i++) {
        arr[i] = arr[i] * num;
    }
}

void subst(float* arr1, float* arr2, int n) {
    int i;
    for(i = 0; i < n; i++) {
        arr1[i] = arr2[i];
    }
}
