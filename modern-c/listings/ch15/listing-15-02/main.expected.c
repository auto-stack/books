// Auto -> C transpiled by a2c
#include <stdio.h>
#include "main.expected.h"

struct Result Result_ok(int val) {
    struct Result r;
    r.value = val;
    r.ok = true;
    return r;
}

struct Result Result_err(void) {
    struct Result r;
    r.value = 0;
    r.ok = false;
    return r;
}

struct Result process(int data) {
    if (data < 0) {
        printf("Invalid input: %d\n", data);
        return Result_err();
    }
    return Result_ok(data * 2);
}

int main(void) {
    struct Result r1 = process(21);
    if (r1.ok) {
        printf("Success: %d\n", r1.value);
    }

    struct Result r2 = process(-5);
    if (!r2.ok) {
        printf("Processing failed\n");
    }

    return 0;
}
