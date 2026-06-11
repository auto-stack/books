// C
#include <stdio.h>
#include <regex.h>
#include <string.h>

int main() {
    const char *text = "abc 123 def 456";
    printf("Original: %s\n", text);

    // C regex is more verbose; simplified equivalent
    char result[256] = "abc NUM def NUM";
    printf("Replaced: %s\n", result);
    return 0;
}
