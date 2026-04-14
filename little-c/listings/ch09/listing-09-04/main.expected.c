// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-09-04.h"

void tokenize(const char *input) {
    printf("%s %s\n", "Tokenizing:", input);
    int tokens = 0;
    int i = 0;
    while (i < (int)strlen(input)) {
        char ch[2] = {input[i], '\0'};
        if (ch[0] == ' ') {
            tokens = tokens + 1;
        }
        i = i + 1;
    }
    tokens = tokens + 1;
    printf("%s %d %s\n", "Found", tokens, "tokens");
}

int main(void) {
    tokenize("hello world foo bar");
    tokenize("one two three");
    return 0;
}
