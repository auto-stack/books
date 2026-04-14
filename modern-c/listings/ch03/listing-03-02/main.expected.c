// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // Counting up
    int sum = 0;
    for (int i = 0; i < 11; i++) {
        sum = sum + i;
    }
    printf("%s %d\n", "Sum 1..10 =", sum);

    // Countdown
    int countdown = 10;
    while (countdown > 0) {
        countdown = countdown - 1;
    }
    printf("%s %d\n", "Countdown done, value:", countdown);

    // Fibonacci
    int a = 0;
    int b = 1;
    for (int i = 0; i < 10; i++) {
        char _tmp0[64];
        snprintf(_tmp0, sizeof(_tmp0), "%s%d%s", "fib(", i, ")");
        printf("%s %d\n", _tmp0, a);
        int temp = a + b;
        a = b;
        b = temp;
    }
    return 0;
}
