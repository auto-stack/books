// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const char* greeting = "Hello, Modern C!";
    const char* name = "Auto";

    printf("Greeting: %s\n", greeting);
    printf("Length: %zu\n", strlen(greeting));

    /* Concatenation */
    /* In C, string concatenation requires buffer management */
    char full[64];
    snprintf(full, sizeof(full), "%s Meet %s.", greeting, name);
    printf("Full: %s\n", full);

    return 0;
}
