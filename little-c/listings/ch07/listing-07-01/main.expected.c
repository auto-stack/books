// Auto → C transpiled by a2c
#include <stdio.h>

int divide(int a, int b) {
    if (b == 0) {
        printf("%s\n", "Error: division by zero");
        return 0;
    }
    return a / b;
}

int main(void) {
    int result = divide(10, 3);
    printf("%s %d\n", "Result:", result);

    int bad = divide(10, 0);
    printf("%s %d\n", "Bad result:", bad);

    printf("%s\n", "Debugging: check return values for errors");
    return 0;
}
