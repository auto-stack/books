// C
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

int clamp(int value, int lo, int hi) {
    if (value < lo) return lo;
    if (value > hi) return hi;
    return value;
}

int main(void) {
    printf("%d\n", 3 < 7 ? 3 : 7);
    printf("%d\n", 3 > 7 ? 3 : 7);
    printf("%d\n", abs(-42));
    printf("%.0f\n", round(3.7));
    printf("%.0f\n", floor(3.9));
    printf("%.0f\n", ceil(3.1));
    printf("%d\n", clamp(15, 0, 10));
    printf("%.0f\n", pow(2.0, 10.0));
    printf("%.0f\n", sqrt(144.0));
    return 0;
}
