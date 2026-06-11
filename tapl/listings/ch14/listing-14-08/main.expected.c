// C
#include <stdio.h>
#include <string.h>

int main() {
    const char *lines[] = {"name,age", "Alice,30", "Bob,25"};
    int num_lines = 3;

    for (int i = 1; i < num_lines; i++) {
        char line[64];
        strncpy(line, lines[i], 64);
        char *name = strtok(line, ",");
        char *age = strtok(NULL, ",");
        printf("Name: %s, Age: %s\n", name, age);
    }
    return 0;
}
