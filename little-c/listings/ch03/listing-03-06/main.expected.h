// Auto → C transpiled by a2c
#ifndef LISTING_03_06_H
#define LISTING_03_06_H

/* spec Drawable vtable */
struct Drawable_vtable {
    void (*draw)(void* self);
};

struct Drawable_base {
    const struct Drawable_vtable* vtable;
};

struct CircleObj {
    struct Drawable_base base;
    float radius;
};

struct SquareObj {
    struct Drawable_base base;
    float side;
};

void CircleObj_draw(struct CircleObj* self);
void SquareObj_draw(struct SquareObj* self);
void render(void* d);

#endif
