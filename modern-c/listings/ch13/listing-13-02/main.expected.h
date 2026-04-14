// Auto -> C transpiled by a2c
#ifndef LISTING_13_02_H
#define LISTING_13_02_H

#include <stdint.h>
#include <stdbool.h>

struct Config {
    char name[256];
    int value;
    bool active;
};

struct Config Config_default(void);
struct Config Config_with_name(const char *name);

#endif
