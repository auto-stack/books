// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    double A[5] = {9.0, 2.9, 0.0, 0.00007, 3e+25};
    for (int i = 0; i < 5; i++) {
        double val = A[i];
        double sq = val * val;
        printf("%s %d %s %f %s %f\n", "element", i, "is", val, ", square is", sq);
    }
    return 0;
}
