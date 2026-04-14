// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void) {
    int x = 42;
    /* C: int *ptr = &x; */
    /* Auto: references are managed, no raw pointers */
    printf("Value: %d\n", x);

    /* Auto's optional type for nullable references */
    int maybe_val = x;
    bool maybe_has = true;
    if (maybe_has) {
        printf("Has value: %d\n", maybe_val);
    }

    return 0;
}
