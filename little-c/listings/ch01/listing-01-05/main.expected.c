// Auto → C transpiled by a2c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int main(void) {
    printf("%s %d\n", "3 + 4 =", add(3, 4));
    printf("%s %d\n", "5! =", factorial(5));
    return 0;
}
