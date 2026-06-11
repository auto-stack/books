// C
#include <stdio.h>
#include <time.h>

int main() {
    clock_t start = clock();

    int sum = 0;
    for (int i = 0; i < 1000; i++) {
        sum += i;
    }

    clock_t end = clock();
    double elapsed = ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;
    printf("Sum: %d\n", sum);
    printf("Elapsed: %.0f ms\n", elapsed);
    printf("Slept 100ms\n");
    return 0;
}
