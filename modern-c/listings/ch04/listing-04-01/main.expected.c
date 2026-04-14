// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int a = 17;
    int b = 5;
    printf("a + b = %d\n", a + b);
    printf("a - b = %d\n", a - b);
    printf("a * b = %d\n", a * b);
    printf("a / b = %d\n", a / b);
    printf("a % b = %d\n", a % b);

    /* Increment/decrement → Auto uses assignment */
    int count = 0;
    count = count + 1;
    count = count + 1;
    count = count + 1;
    printf("Count: %d\n", count);

    return 0;
}
