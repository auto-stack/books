// C
#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    return *(int*)a - *(int*)b;
}

int main() {
    int nums[] = {15, 3, 8, 1, 12, 7};
    int len = 6;

    printf("Before sort:\n");
    for (int i = 0; i < len; i++) printf("%d ", nums[i]);
    printf("\n");

    qsort(nums, len, sizeof(int), cmp);

    printf("After sort:\n");
    for (int i = 0; i < len; i++) printf("%d ", nums[i]);
    printf("\n");
    return 0;
}
