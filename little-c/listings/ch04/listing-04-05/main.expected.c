// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "listing-04-05.h"

struct LogEntry LogEntry_new(const char* level, const char* message) {
    struct LogEntry e;
    e.level = strdup(level);
    e.message = strdup(message);
    return e;
}

static char* str_concat3(const char* a, const char* b, const char* c) {
    size_t len = strlen(a) + strlen(b) + strlen(c) + 1;
    char* buf = (char*)malloc(len);
    strcpy(buf, a);
    strcat(buf, b);
    strcat(buf, c);
    return buf;
}

int main(void) {
    struct LogEntry e1 = LogEntry_new("INFO", "Server started");
    struct LogEntry e2 = LogEntry_new("WARN", "Low memory");
    struct LogEntry e3 = LogEntry_new("ERROR", "Disk full");

    char* line1 = str_concat3("[", e1.level, "] ");
    char* line1b = str_concat3(line1, e1.message, "");
    printf("%s\n", line1b);
    free(line1); free(line1b);

    char* line2 = str_concat3("[", e2.level, "] ");
    char* line2b = str_concat3(line2, e2.message, "");
    printf("%s\n", line2b);
    free(line2); free(line2b);

    char* line3 = str_concat3("[", e3.level, "] ");
    char* line3b = str_concat3(line3, e3.message, "");
    printf("%s\n", line3b);
    free(line3); free(line3b);

    return 0;
}
