// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include "main.expected.h"

struct Fraction Fraction_new(int n, int d) {
    struct Fraction f;
    f.num = n;
    f.den = d;
    return f;
}

float Fraction_to_float(struct Fraction f) {
    return (float)f.num / (float)f.den;
}

int main(void) {
    struct Fraction half = Fraction_new(1, 2);
    struct Fraction third = Fraction_new(1, 3);
    printf("1/2 = %f\n", Fraction_to_float(half));
    printf("1/3 = %f\n", Fraction_to_float(third));

    return 0;
}
