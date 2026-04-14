// Auto → C transpiled by a2c
#ifndef LISTING_03_02_H
#define LISTING_03_02_H

enum Shape_tag {
    SHAPE_CIRCLE,
    SHAPE_RECT,
    SHAPE_TRIANGLE
};

struct Shape {
    enum Shape_tag tag;
    union {
        float Circle;
        float Rect[2];
        float Triangle[3];
    } as;
};

float area(struct Shape s);

#endif
