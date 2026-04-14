// Auto → C transpiled by a2c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main(void) {
    int sum = add(3, 4);
    int product = multiply(3, 4);
    printf("%s %d\n", "Sum:", sum);
    printf("%s %d\n", "Product:", product);
    return 0;
}
