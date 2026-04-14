// Auto → C transpiled by a2c
#include <stdio.h>

char* classify(int n) {
    if (n > 0) {
        return "positive";
    } else if (n < 0) {
        return "negative";
    } else {
        return "zero";
    }
}

char* describe(int x) {
    switch (x) {
        case 0: return "nothing";
        case 1: return "one";
        case 2: return "two";
        default: return "many";
    }
}

int main(void) {
    printf("%s\n", classify(5));
    printf("%s\n", classify(-3));
    printf("%s\n", classify(0));
    printf("%s\n", describe(0));
    printf("%s\n", describe(1));
    printf("%s\n", describe(5));
    return 0;
}
