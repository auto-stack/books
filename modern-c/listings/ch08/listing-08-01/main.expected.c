// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int a = 17;
    int b = 5;

    /* C: div_t result = div(17, 5); */
    printf("Quotient: %d\n", a / b);
    printf("Remainder: %d\n", a % b);
    printf("Absolute: %d\n", abs(-42));

    /* Bounds checking (Modern C emphasis) */
    int large = 2147483647;
    printf("Large int: %d\n", large);

    return 0;
}
