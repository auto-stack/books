// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int primes[5] = {2, 3, 5, 7, 11};
    for (int i = 0; i < 5; i++) {
        printf("primes[%d] = %d\n", i, primes[i]);
    }

    /* Sum of array */
    int total = 0;
    for (int i = 0; i < 5; i++) {
        total = total + primes[i];
    }
    printf("Sum of primes: %d\n", total);

    return 0;
}
