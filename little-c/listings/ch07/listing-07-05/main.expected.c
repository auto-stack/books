// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdbool.h>

int sum_to(int n) {
    int total = 0;
    for (int i = 0; i < n + 1; i++) {
        total = total + i;
    }
    return total;
}

bool is_positive(int n) {
    return n > 0;
}

int fib(int n) {
    if (n <= 0) { return 0; }
    if (n == 1) { return 1; }
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    printf("%s %d\n", "Sum 1..10 =", sum_to(10));
    printf("%s %d\n", "is_positive(5):", is_positive(5));
    printf("%s %d\n", "is_positive(-1):", is_positive(-1));
    printf("%s %d\n", "fib(10) =", fib(10));
    return 0;
}
