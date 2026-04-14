// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    for (int i = 0; i < 5; i++) {
        printf("%s %d\n", "i =", i);
    }

    int sum = 0;
    int n = 1;
    while (n <= 10) {
        sum = sum + n;
        n = n + 1;
    }
    printf("%s %d\n", "Sum 1..10 =", sum);
    return 0;
}
