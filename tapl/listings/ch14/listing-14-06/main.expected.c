// C
#include <stdio.h>
#include <string.h>

int main() {
    FILE *f = fopen("lines.txt", "w");
    fprintf(f, "Rust\nFun\nAuto");
    fclose(f);

    f = fopen("lines.txt", "r");
    char buf[256];
    int n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);

    printf("Content: %s\n", buf);
    printf("Length: %d\n", n);

    char *line = strtok(buf, "\n");
    while (line != NULL) {
        printf("  Line: %s\n", line);
        line = strtok(NULL, "\n");
    }

    remove("lines.txt");
    return 0;
}
