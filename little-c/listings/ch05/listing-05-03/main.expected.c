// Auto → C transpiled by a2c
#include <stdio.h>

void greet(const char* name) {
    printf("%s %s\n", "Hello,", name);
}

void farewell(const char* name) {
    printf("%s %s\n", "Goodbye,", name);
}

int main(void) {
    greet("World");
    farewell("World");
    return 0;
}
