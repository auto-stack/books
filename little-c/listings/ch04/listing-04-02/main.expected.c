// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

static void write_file(const char* path, const char* content) {
    FILE* f = fopen(path, "w");
    if (!f) return;
    fputs(content, f);
    fclose(f);
}

static char* read_file(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* buf = (char*)malloc(len + 1);
    fread(buf, 1, len, f);
    buf[len] = '\0';
    fclose(f);
    return buf;
}

int main(void) {
    char* content = "Hello from Auto\nLine 2\nLine 3\n";
    write_file("output.txt", content);
    printf("%s\n", "Written to output.txt");

    char* data = read_file("output.txt");
    printf("%s %s\n", "Read back:", data);
    free(data);
    return 0;
}
