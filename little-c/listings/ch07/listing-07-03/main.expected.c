// Auto → C transpiled by a2c
#include <stdio.h>
#include <assert.h>

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int main(void) {
    assert(add(2, 3) == 5 && "add test");
    assert(subtract(5, 3) == 2 && "subtract test");
    assert(multiply(3, 4) == 12 && "multiply test");
    printf("%s\n", "All tests passed!");
    return 0;
}
