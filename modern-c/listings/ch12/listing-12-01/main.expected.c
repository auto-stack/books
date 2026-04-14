// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "main.expected.h"

const char* describe(struct Value v) {
    static char buf[128];
    switch (v.tag) {
        case VAL_INT:
            snprintf(buf, sizeof(buf), "integer: %d", v.data.i);
            return buf;
        case VAL_FLOAT:
            snprintf(buf, sizeof(buf), "float: %f", v.data.f);
            return buf;
        case VAL_STR:
            snprintf(buf, sizeof(buf), "string: %s", v.data.s);
            return buf;
    }
    return "";
}

int main(void) {
    struct Value a;
    a.tag = VAL_INT;
    a.data.i = 42;

    struct Value b;
    b.tag = VAL_FLOAT;
    b.data.f = 3.14f;

    struct Value c;
    c.tag = VAL_STR;
    snprintf(c.data.s, sizeof(c.data.s), "hello");

    printf("%s\n", describe(a));
    printf("%s\n", describe(b));
    printf("%s\n", describe(c));

    return 0;
}
