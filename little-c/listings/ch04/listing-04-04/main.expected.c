// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("%s\n", "Usage: program <name>");
        return 0;
    }
    char* name = argv[1];
    printf("%s %s\n", "Hello,", name);
    printf("%s %d\n", "Argument count:", argc);
    return 0;
}
