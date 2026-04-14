// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main(void) {
    for (int i = 0; i < 10; i++) {
        /* str(i) allocation */
        char buf[16];
        snprintf(buf, sizeof(buf), "%d", i);
        /* greeting + str(i) + greeting concatenation */
        char* tmp = malloc(strlen("fib(") + strlen(buf) + strlen(") = ") + 1);
        strcpy(tmp, "fib(");
        strcat(tmp, buf);
        strcat(tmp, ") = ");
        printf("%s %d\n", tmp, fibonacci(i));
        free(tmp);
    }
    return 0;
}
