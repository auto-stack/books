// Auto → C transpiled by a2c
#include <stdio.h>
#include <math.h>
#include "main.expected.h"

float Point_distance_from_origin(struct Point p) {
    return sqrtf(p.x * p.x + p.y * p.y);
}

struct Point Point_translate(struct Point p, float dx, float dy) {
    struct Point result;
    result.x = p.x + dx;
    result.y = p.y + dy;
    return result;
}

int main(void) {
    struct Point p;
    p.x = 3.0f;
    p.y = 4.0f;
    printf("Point: %f %f\n", p.x, p.y);
    printf("Distance from origin: %f\n", Point_distance_from_origin(p));

    struct Point moved = Point_translate(p, 1.0f, 2.0f);
    printf("Moved to: %f %f\n", moved.x, moved.y);

    return 0;
}
