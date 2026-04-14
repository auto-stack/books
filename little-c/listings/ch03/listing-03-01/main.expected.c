// Auto → C transpiled by a2c
#include <stdio.h>
#include "listing-03-01.h"

float Point_Modulus(struct Point *self) {
    return (float)(self->x * self->x + self->y * self->y);
}

int main(void) {
    struct Point p = (struct Point){.x = 3, .y = 4};
    printf("%s %s %d %s %d %s\n", "Point: (", p.x, ",", p.y, ")");
    printf("%s %f\n", "Modulus:", Point_Modulus(&p));
    return 0;
}
