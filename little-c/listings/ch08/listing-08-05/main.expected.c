// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "listing-08-05.h"

int is_little_endian(void) {
    uint32_t val = 1;
    uint8_t *bytes = (uint8_t *)&val;
    return bytes[0] == 1;
}

int main(void) {
    if (is_little_endian()) {
        printf("%s\n", "System is little-endian");
    } else {
        printf("%s\n", "System is big-endian");
    }
    printf("%s\n", "Auto handles endianness automatically");
    printf("%s\n", "Generated C code is portable across platforms");
    return 0;
}
