// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("%s\n", "Usage: todo <command> [args]");
        printf("%s\n", "Commands: add, list, done");
        return 0;
    }

    const char *cmd = argv[1];
    if (strcmp(cmd, "add") == 0) {
        printf("%s\n", "Adding task...");
    } else if (strcmp(cmd, "list") == 0) {
        printf("%s\n", "Listing tasks...");
    } else if (strcmp(cmd, "done") == 0) {
        printf("%s\n", "Completing task...");
    } else {
        printf("%s %s\n", "Unknown command:", cmd);
    }
    return 0;
}
