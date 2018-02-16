#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif
extern void scaling(int, float*, int);
#ifdef __cplusplus
}
#endif

void scaling(int num, float* arr, int size) {
    int i;
    for(i = 0; i < size; i++) {
        arr[i] = arr[i] * num;
    }
}
