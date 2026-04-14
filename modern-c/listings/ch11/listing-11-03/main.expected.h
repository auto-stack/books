// Auto → C transpiled by a2c
#ifndef LISTING_11_03_H
#define LISTING_11_03_H

/* Comparator spec vtable */
struct Comparator_vtable {
    int (*compare)(int a, int b);
};

struct Ascending {
    const struct Comparator_vtable* vtable;
};

struct Descending {
    const struct Comparator_vtable* vtable;
};

const struct Comparator_vtable* Comparator_vtable(const void* self);

int Ascending_compare(int a, int b);
int Descending_compare(int a, int b);

#endif
