// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include "main.expected.h"

int main(void) {
    float pi = 3.14159f;      /* immutable constant (let) */
    int max_size = 1024;

    printf("PI: %f\n", pi);
    printf("Max size: %d\n", max_size);

    enum Direction d = North;
    printf("Direction: %d\n", (int)d);

    return 0;
}
