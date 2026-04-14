// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    /* C Deep Dive: effective types and strict aliasing */
    /* C: int x; float *fp = (float*)&x; // UB! */
    /* Auto prevents type punning by design */

    int x = 42;
    float f = (float)x;  /* safe conversion */
    printf("int to float: %f\n", f);

    /* Alignment in C: alignas(16) int x; */
    /* Auto handles alignment automatically */
    printf("Auto handles memory alignment automatically\n");
    printf("No type punning — conversions are explicit and safe\n");

    return 0;
}
