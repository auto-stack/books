// C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    const char *lines[] = {"name,age", "Alice,30", "Bob,25", "Charlie,35"};
    int num_lines = 4;

    printf("People over 28:\n");
    for (int i = 1; i < num_lines; i++) {
        char line[64];
        strncpy(line, lines[i], 64);
        char *name = strtok(line, ",");
        char *age_str = strtok(NULL, ",");
        int age = atoi(age_str);
        if (age > 28) {
            printf("  %s (%d)\n", name, age);
        }
    }
    return 0;
}
