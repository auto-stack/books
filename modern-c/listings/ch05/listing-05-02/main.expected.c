// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    /* Implicit conversion: int → float */
    int n = 42;
    float f = (float)n;       /* explicit cast */
    printf("int as float: %f\n", f);

    /* Float → int (truncation) */
    float pi = 3.14159f;
    int truncated = (int)pi;
    printf("truncated pi: %d\n", truncated);

    return 0;
}
