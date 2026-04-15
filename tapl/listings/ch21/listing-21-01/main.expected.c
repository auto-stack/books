// C
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

void to_upper_copy(const char* src, char* dst, int max_len) {
    int i;
    for (i = 0; src[i] && i < max_len - 1; i++) {
        dst[i] = toupper((unsigned char)src[i]);
    }
    dst[i] = '\0';
}

void replace_str(const char* src, const char* old_s, const char* new_s,
                 char* dst, int max_len) {
    int src_len = strlen(src);
    int old_len = strlen(old_s);
    int new_len = strlen(new_s);
    int pos = 0, i = 0;
    while (i < src_len && pos < max_len - 1) {
        if (strncmp(src + i, old_s, old_len) == 0) {
            for (int j = 0; j < new_len && pos < max_len - 1; j++) {
                dst[pos++] = new_s[j];
            }
            i += old_len;
        } else {
            dst[pos++] = src[i++];
        }
    }
    dst[pos] = '\0';
}

void trim_copy(const char* src, char* dst, int max_len) {
    while (*src == ' ' || *src == '\t' || *src == '\n') src++;
    int len = strlen(src);
    while (len > 0 && (src[len-1] == ' ' || src[len-1] == '\t' || src[len-1] == '\n'))
        len--;
    int copy_len = len < max_len - 1 ? len : max_len - 1;
    strncpy(dst, src, copy_len);
    dst[copy_len] = '\0';
}

int main(void) {
    char trimmed[64];
    trim_copy("  Hello, World!  ", trimmed, 64);
    printf("%s\n", trimmed);

    printf("Hello, %s!\n", "Auto");

    const char* csv = "one,two,three,four";
    char csv_copy[64];
    strncpy(csv_copy, csv, 64);
    char* token = strtok(csv_copy, ",");
    while (token != NULL) {
        printf("%s\n", token);
        token = strtok(NULL, ",");
    }

    printf("Hello World\n");

    const char* msg = "Hello, World!";
    printf("%d\n", strstr(msg, "World") != NULL);
    printf("%d\n", strncmp(msg, "Hello", 5) == 0);
    int msg_len = strlen(msg);
    printf("%d\n", msg[msg_len - 1] == '!');
    char upper[64];
    to_upper_copy(msg, upper, 64);
    printf("%s\n", upper);
    char replaced[64];
    replace_str(msg, "World", "Auto", replaced, 64);
    printf("%s\n", replaced);
    return 0;
}
