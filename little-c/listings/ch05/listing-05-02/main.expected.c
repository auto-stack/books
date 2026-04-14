// Auto → C transpiled by a2c
#include <stdio.h>

int max(int a, int b) {
    if (a > b) { return a; } else { return b; }
}

int main(void) {
    float pi = 3.14159f;
    float radius = 5.0f;
    float area = pi * radius * radius;
    printf("%s %f\n", "Area:", area);

    int larger = max(10, 20);
    printf("%s %d\n", "Max:", larger);
    return 0;
}
