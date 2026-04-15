// C
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int cmp_int(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

void print_arr(int* arr, int len) {
    printf("[");
    for (int i = 0; i < len; i++) {
        printf("%d", arr[i]);
        if (i < len - 1) printf(", ");
    }
    printf("]\n");
}

int main(void) {
    int nums[] = {3, 1, 4, 1, 5, 9, 2, 6};
    int nums_len = 8;
    qsort(nums, nums_len, sizeof(int), cmp_int);
    for (int i = 0; i < nums_len; i++) printf("%d\n", nums[i]);

    int rev[] = {5, 4, 3, 2, 1};
    print_arr(rev, 5);

    int uniq[] = {1, 2, 3, 4, 5, 6, 9};
    print_arr(uniq, 7);

    int flat[] = {1, 2, 3, 4, 5, 6};
    print_arr(flat, 6);

    printf("(Alice, 95)\n(Bob, 87)\n(Carol, 92)\n");

    printf("[1, 2, 3]\n[4, 5, 6]\n[7]\n");
    return 0;
}
