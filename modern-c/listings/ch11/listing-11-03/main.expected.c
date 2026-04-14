// Auto → C transpiled by a2c
#include <stdio.h>
#include "main.expected.h"

int Ascending_compare(int a, int b) {
    if (a < b) { return -1; }
    else if (a > b) { return 1; }
    else { return 0; }
}

int Descending_compare(int a, int b) {
    if (a > b) { return -1; }
    else if (a < b) { return 1; }
    else { return 0; }
}

int main(void) {
    struct Ascending asc;
    struct Descending desc;

    printf("Asc compare(3,7): %d\n", Comparator_vtable(&asc)->compare(3, 7));
    printf("Desc compare(3,7): %d\n", Comparator_vtable(&desc)->compare(3, 7));

    return 0;
}
