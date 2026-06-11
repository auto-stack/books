// C
#include <stdio.h>
#include <string.h>

int main() {
    const char *path = "test_temp.txt";

    FILE *f = fopen(path, "w");
    fprintf(f, "line1\nline2\nline3");
    fclose(f);

    f = fopen(path, "r");
    char buf[256];
    int n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);

    int line_count = 0;
    char *line = strtok(buf, "\n");
    while (line != NULL) {
        line_count++;
        printf("  [%d] %s\n", line_count, line);
        line = strtok(NULL, "\n");
    }
    printf("Total lines: %d\n", line_count);

    remove(path);
    return 0;
}
