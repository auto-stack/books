// Auto → C transpiled by a2c
#include <stdio.h>

void greet(const char* name) {
    printf("%s %s\n", "Hello,", name);
}

int main(void) {
    int count = 0;
    for (int i = 0; i < 5; i++) {
        count = count + 1;
    }
    printf("%s %d\n", "Count:", count);
    greet("Modern C");
    return 0;
}
