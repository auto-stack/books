// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int x = 42;
    int y = 0;

    /* Boolean context: truth values */
    if (x) {
        printf("x is truthy\n");
    }
    if (!y) {
        printf("y is falsy (zero)\n");
    }

    /* Ternary → if/else expression */
    const char* label = (x > 0) ? "positive" : "non-positive";
    printf("x is %s\n", label);

    return 0;
}
