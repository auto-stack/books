// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    int x = 42;
    /* C: int *ptr = &x; *ptr = 99; */
    /* Auto: no raw pointers, direct value access */
    printf("Value: %d\n", x);

    /* Pointer arithmetic in C: */
    /* int arr[5]; int *p = arr; p += 3; */
    /* Auto: use array indexing */
    int arr[5] = {10, 20, 30, 40, 50};
    printf("arr[3]: %d\n", arr[3]);

    /* C Deep Dive: pointer subtraction gives distance */
    printf("Array access replaces pointer arithmetic\n");

    return 0;
}
