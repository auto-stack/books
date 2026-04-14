// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char* content = "Sample file content\nWith multiple lines\n";

    /* write_file: Auto high-level wrapper */
    FILE* wf = fopen("sample.txt", "w");
    if (wf) {
        fputs(content, wf);
        fclose(wf);
    }
    printf("%s\n", "Wrote sample file");

    /* read_file: Auto high-level wrapper */
    char* read_back = NULL;
    FILE* rf = fopen("sample.txt", "r");
    if (rf) {
        fseek(rf, 0, SEEK_END);
        long len = ftell(rf);
        fseek(rf, 0, SEEK_SET);
        read_back = malloc(len + 1);
        if (read_back) {
            fread(read_back, 1, len, rf);
            read_back[len] = '\0';
        }
        fclose(rf);
    }
    printf("%s %s\n", "Read:", read_back ? read_back : "(null)");
    free(read_back);
    return 0;
}
