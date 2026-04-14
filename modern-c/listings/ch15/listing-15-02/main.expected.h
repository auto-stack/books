// Auto -> C transpiled by a2c
#ifndef LISTING_15_02_H
#define LISTING_15_02_H

#include <stdbool.h>

struct Result {
    int value;
    bool ok;
};

struct Result Result_ok(int val);
struct Result Result_err(void);
struct Result process(int data);

#endif
