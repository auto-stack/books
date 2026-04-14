// Auto → C transpiled by a2c
#include <stdio.h>

/* spec IntOp vtable */
struct IntOp_vtable {
    int (*apply)(int a, int b);
};

struct Adder {
    const struct IntOp_vtable* vtable;
};

int Adder_apply(int a, int b) {
    return a + b;
}

static const struct IntOp_vtable Adder_vtable = {
    .apply = Adder_apply,
};

struct Multiplier {
    const struct IntOp_vtable* vtable;
};

int Multiplier_apply(int a, int b) {
    return a * b;
}

static const struct IntOp_vtable Multiplier_vtable = {
    .apply = Multiplier_apply,
};

int compute(struct Adder* op, int a, int b) {
    return op->vtable->apply(a, b);
}

int main(void) {
    struct Adder adder = {&Adder_vtable};
    struct Multiplier mult = {&Multiplier_vtable};
    printf("%s %d\n", "3 + 4 =", compute(&adder, 3, 4));
    return 0;
}
