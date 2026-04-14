// Auto -> C transpiled by a2c
#include <stdio.h>

int safe_divide(int a, int b) {
    if (b == 0) {
        printf("Error: division by zero\n");
        return 0;
    }
    return a / b;
}

int safe_access(const int arr[5], int index) {
    if (index < 0 || index >= 5) {
        printf("Error: index out of bounds\n");
        return 0;
    }
    return arr[index];
}

int main(void) {
    printf("10 / 3 = %d\n", safe_divide(10, 3));
    printf("10 / 0 = %d\n", safe_divide(10, 0));

    int data[5] = {10, 20, 30, 40, 50};
    printf("data[2] = %d\n", safe_access(data, 2));
    printf("data[10] = %d\n", safe_access(data, 10));

    return 0;
}
