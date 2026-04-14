// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-05-05.h"

struct Counter Counter_new(void) {
    struct Counter c;
    memset(&c, 0, sizeof(c));
    c.count = 0;
    return c;
}

void Counter_increment(struct Counter* c) {
    c->count = c->count + 1;
}

int Counter_value(struct Counter* c) {
    return c->count;
}

int main(void) {
    struct Counter c = Counter_new();
    Counter_increment(&c);
    Counter_increment(&c);
    Counter_increment(&c);
    printf("%s %d\n", "Count:", Counter_value(&c));
    return 0;
}
