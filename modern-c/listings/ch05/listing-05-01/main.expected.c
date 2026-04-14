// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void) {
    /* Basic types mapping */
    char c = 'A';                       /* char */
    int i = 42;                         /* int (signed) */
    float f = 3.14f;                    /* float */
    double d = 2.718;                   /* double → Auto float */
    bool b = true;                      /* bool */
    const char* s = "hello";            /* char* string */

    printf("char: %c\n", c);
    printf("int: %d\n", i);
    printf("float: %f\n", f);
    printf("double: %f\n", d);
    printf("bool: %s\n", b ? "true" : "false");
    printf("string: %s\n", s);

    return 0;
}
