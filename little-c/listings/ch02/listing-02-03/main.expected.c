// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    int scores[5] = {90, 85, 78, 92, 88};
    for (int i = 0; i < 5; i++) {
        printf("%s %d %s %d\n", "Score", i, "=", scores[i]);
    }
    printf("%s\n", "First three printed via loop");
    for (int i = 0; i < 3; i++) {
        printf("%d\n", scores[i]);
    }
    return 0;
}
