// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>

int calculate(int a, char* op, int b) {
    if (strcmp(op, "+") == 0) {
        return a + b;
    } else if (strcmp(op, "-") == 0) {
        return a - b;
    } else if (strcmp(op, "*") == 0) {
        return a * b;
    } else if (strcmp(op, "/") == 0) {
        if (b == 0) {
            printf("%s\n", "Error: division by zero");
            return 0;
        } else {
            return a / b;
        }
    } else {
        printf("%s %s\n", "Unknown operator:", op);
        return 0;
    }
}

int main(void) {
    printf("%s %d\n", "10 + 3 =", calculate(10, "+", 3));
    printf("%s %d\n", "10 - 3 =", calculate(10, "-", 3));
    printf("%s %d\n", "10 * 3 =", calculate(10, "*", 3));
    printf("%s %d\n", "10 / 3 =", calculate(10, "/", 3));
    printf("%s %d\n", "10 / 0 =", calculate(10, "/", 0));
    return 0;
}
