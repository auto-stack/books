// C
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

void path_join(const char* dir, const char* file, char* out, int max) {
    snprintf(out, max, "%s/%s", dir, file);
}

int main(void) {
    char path[256];
    path_join("data", "output.txt", path, 256);
    printf("%s\n", path);

    FILE* f = fopen(path, "w");
    if (f) { fprintf(f, "Hello from Auto!"); fclose(f); }
    f = fopen(path, "r");
    if (f) {
        char buf[256];
        int n = fread(buf, 1, sizeof(buf) - 1, f);
        buf[n] = '\0';
        printf("%s\n", buf);
        fclose(f);
    }

    struct stat st;
    printf("%d\n", stat(path, &st) == 0);
    printf("%d\n", stat("nonexistent.txt", &st) == 0);

    mkdir("data/backup", 0755);
    DIR* d = opendir("data");
    if (d) {
        struct dirent* entry;
        while ((entry = readdir(d)) != NULL) {
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0)
                printf("%s\n", entry->d_name);
        }
        closedir(d);
    }
    return 0;
}
