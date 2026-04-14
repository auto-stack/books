// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char* greeting = "Hello";
    char* name = "World";
    char* full = malloc(strlen(greeting) + 1 + strlen(name) + 1);
    strcpy(full, greeting);
    strcat(full, " ");
    strcat(full, name);
    printf("%s\n", full);
    printf("%s %d\n", "Length:", (int)strlen(full));
    free(full);
    return 0;
}
