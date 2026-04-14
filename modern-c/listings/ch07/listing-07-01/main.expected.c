// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int max(int a, int b) {
    return (a > b) ? a : b;
}

int min(int a, int b) {
    return (a < b) ? a : b;
}

int clamp(int val, int lo, int hi) {
    return max(lo, min(val, hi));
}

int main(void) {
    printf("max(3, 7) = %d\n", max(3, 7));
    printf("clamp(15, 0, 10) = %d\n", clamp(15, 0, 10));
    printf("clamp(-5, 0, 10) = %d\n", clamp(-5, 0, 10));

    return 0;
}
