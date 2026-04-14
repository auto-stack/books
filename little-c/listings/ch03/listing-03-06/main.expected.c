// Auto → C transpiled by a2c
#include <stdio.h>
#include "listing-03-06.h"

/* Drawable vtable */
static const struct Drawable_vtable Drawable_vtable_instance;

void CircleObj_draw(struct CircleObj* self) {
    printf("%s %f\n", "Drawing circle with radius:", self->radius);
}

static const struct Drawable_vtable CircleObj_vtable = {
    .draw = (void (*)(void*))CircleObj_draw,
};

void SquareObj_draw(struct SquareObj* self) {
    printf("%s %f\n", "Drawing square with side:", self->side);
}

static const struct Drawable_vtable SquareObj_vtable = {
    .draw = (void (*)(void*))SquareObj_draw,
};

void render(void* d) {
    struct Drawable_base* base = (struct Drawable_base*)d;
    base->vtable->draw(d);
}

int main(void) {
    struct CircleObj c = {.base = {.vtable = &CircleObj_vtable}, .radius = 5.0f};
    struct SquareObj s = {.base = {.vtable = &SquareObj_vtable}, .side = 3.0f};
    render(&c);
    render(&s);
    return 0;
}
