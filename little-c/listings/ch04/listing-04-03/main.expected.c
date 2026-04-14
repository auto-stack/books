// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-04-03.h"

int main(void) {
    struct Record r = (struct Record){.id = 1, .value = 3.14f};
    printf("%s %d\n", "Record id:", r.id);
    printf("%s %f\n", "Record value:", r.value);
    return 0;
}
