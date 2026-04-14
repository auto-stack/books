// Auto → C transpiled by a2c
#ifndef LISTING_12_01_H
#define LISTING_12_01_H

enum ValueTag {
    VAL_INT,
    VAL_FLOAT,
    VAL_STR
};

struct ValueData {
    int i;
    float f;
    char s[256];
};

struct Value {
    enum ValueTag tag;
    struct ValueData data;
};

const char* describe(struct Value v);

#endif
