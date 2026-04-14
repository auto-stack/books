// Auto → C transpiled by a2c
#include <stdio.h>

float calculate_area(float width, float height) {
    return width * height;
}

float calculate_perimeter(float width, float height) {
    return 2.0 * (width + height);
}

int main(void) {
    float width = 5.0f;
    float height = 3.0f;
    printf("Rectangle %f x %f\n", width, height);
    printf("Area: %f\n", calculate_area(width, height));
    printf("Perimeter: %f\n", calculate_perimeter(width, height));

    return 0;
}
