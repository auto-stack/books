// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char* name = "Modern C";
    double version = 2.0;
    int year = 2024;

    /* C uses printf with format specifiers */
    /* Auto's print infers types automatically */
    printf("Book: %s\n", name);
    printf("Version: %f\n", version);
    printf("Year: %d\n", year);

    /* Multi-argument print */
    printf("%s version %f published in %d\n", name, version, year);

    return 0;
}
