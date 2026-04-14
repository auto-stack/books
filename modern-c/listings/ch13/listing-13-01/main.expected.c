// Auto -> C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "main.expected.h"

struct Buffer Buffer_new(void) {
    struct Buffer b;
    memset(b.data, 0, sizeof(b.data));
    b.size = 0;
    return b;
}

void Buffer_push(struct Buffer b, int val) {
    if (b.size < 256) {
        b.data[b.size] = val;
        b.size = b.size + 1;
    }
}

int main(void) {
    /* C: Buffer *b = malloc(sizeof(Buffer)); ... free(b); */
    /* Auto: automatic storage, no malloc/free needed */
    struct Buffer b = Buffer_new();
    for (int i = 0; i < 10; i++) {
        Buffer_push(b, i * i);
    }
    printf("Buffer size: %d\n", b.size);
    printf("First element: %d\n", b.data[0]);
    printf("Last element: %d\n", b.data[b.size - 1]);

    return 0;
}
