// Auto → C transpiled by a2c
#include <stdio.h>

const char* classify(int n) {
    if (n > 0) {
        return "positive";
    } else if (n < 0) {
        return "negative";
    } else {
        return "zero";
    }
}

int main(void) {
    int values[5] = {3, -1, 0, 7, -5};
    for (int i = 0; i < 5; i++) {
        printf("%s %d %s %s\n", "Value", values[i], "is", classify(values[i]));
    }
    return 0;
}
