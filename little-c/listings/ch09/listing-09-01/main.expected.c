// Auto → C transpiled by a2c
#include <stdio.h>
#include <math.h>
#include "listing-09-01.h"

struct Vec2 Vec2_new(float x, float y) {
    return (struct Vec2){.x = x, .y = y};
}

struct Vec2 Vec2_add(struct Vec2 a, struct Vec2 b) {
    return (struct Vec2){.x = a.x + b.x, .y = a.y + b.y};
}

float Vec2_length(struct Vec2 v) {
    return sqrtf(v.x * v.x + v.y * v.y);
}

int main(void) {
    struct Vec2 a = Vec2_new(3.0f, 4.0f);
    struct Vec2 b = Vec2_new(1.0f, 2.0f);
    struct Vec2 c = Vec2_add(a, b);
    printf("%s %f %s %f %s\n", "a + b = (", c.x, ",", c.y, ")");
    printf("%s %f\n", "|a| =", Vec2_length(a));
    return 0;
}
