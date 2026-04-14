// Auto -> C transpiled by a2c
#ifndef LISTING_13_01_H
#define LISTING_13_01_H

#include <stdint.h>

struct Buffer {
    int data[256];
    int size;
};

struct Buffer Buffer_new(void);
void Buffer_push(struct Buffer b, int val);

#endif
