// Auto → C transpiled by a2c
#include <stdio.h>
#include "main.expected.h"

struct Rectangle Rectangle_new(float w, float h) {
    struct Rectangle r;
    r.width = w;
    r.height = h;
    return r;
}

float Rectangle_area(struct Rectangle r) {
    return r.width * r.height;
}

float Rectangle_perimeter(struct Rectangle r) {
    return 2.0f * (r.width + r.height);
}

int main(void) {
    struct Rectangle r = Rectangle_new(4.0f, 6.0f);
    printf("Area: %f\n", Rectangle_area(r));
    printf("Perimeter: %f\n", Rectangle_perimeter(r));

    return 0;
}
