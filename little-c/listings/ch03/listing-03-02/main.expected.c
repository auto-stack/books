// Auto → C transpiled by a2c
#include <stdio.h>
#include <math.h>
#include "listing-03-02.h"

float area(struct Shape s) {
    switch (s.tag) {
        case SHAPE_CIRCLE: {
            float r = s.as.Circle;
            return 3.14159f * r * r;
        }
        case SHAPE_RECT: {
            float w = s.as.Rect[0];
            float h = s.as.Rect[1];
            return w * h;
        }
        case SHAPE_TRIANGLE: {
            float a = s.as.Triangle[0];
            float b = s.as.Triangle[1];
            float c = s.as.Triangle[2];
            float s = (a + b + c) / 2.0f;
            return sqrtf(s * (s - a) * (s - b) * (s - c));
        }
    }
    return 0.0f;
}

int main(void) {
    struct Shape c = (struct Shape){.tag = SHAPE_CIRCLE, .as.Circle = 5.0f};
    struct Shape r = (struct Shape){.tag = SHAPE_RECT, .as.Rect = {3.0f, 4.0f}};
    printf("%s %f\n", "Circle area:", area(c));
    printf("%s %f\n", "Rect area:", area(r));
    return 0;
}
