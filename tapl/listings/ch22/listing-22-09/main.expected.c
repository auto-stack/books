// C
#include <stdio.h>

int main() {
    const char *lines[] = {
        "Building project...",
        "Compiling src/main.at",
        "Done: 2 files compiled"
    };
    int count = 3;

    printf("Captured %d lines:\n", count);
    for (int i = 0; i < count; i++) {
        printf("  %s\n", lines[i]);
    }
    return 0;
}
