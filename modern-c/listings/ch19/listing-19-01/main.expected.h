// Auto -> C transpiled by a2c
#ifndef LISTING_19_01_H
#define LISTING_19_01_H

#include <stdbool.h>

struct ParseResult {
    int value;
    bool ok;
    const char *error;
};

struct ParseResult ParseResult_ok(int val);
struct ParseResult ParseResult_err(const char *msg);
struct ParseResult parse_positive(const char *s);

#endif
