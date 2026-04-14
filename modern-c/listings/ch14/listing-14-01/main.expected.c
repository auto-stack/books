// Auto -> C transpiled by a2c
#include <stdio.h>
#include <string.h>

int count_words(const char *text) {
    int count = 0;
    int in_word = 0;
    size_t text_len = strlen(text);
    for (size_t i = 0; i < text_len; i++) {
        char ch = text[i];
        if (ch == ' ') {
            in_word = 0;
        } else {
            if (!in_word) {
                count = count + 1;
            }
            in_word = 1;
        }
    }
    return count;
}

int main(void) {
    const char *text = "Modern C is a rigorous programming language";
    printf("Text: %s\n", text);
    printf("Word count: %d\n", count_words(text));
    printf("Character count: %zu\n", strlen(text));

    return 0;
}
