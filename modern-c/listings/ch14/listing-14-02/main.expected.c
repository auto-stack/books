// Auto -> C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>

int parse_int(const char *s) {
    /* C: sscanf(s, "%d", &result); */
    /* Auto: str to int conversion */
    int result = atoi(s);
    return result;
}

int main(void) {
    /* Simulating input parsing */
    const char *input = "42";
    int value = parse_int(input);
    printf("Parsed: %d\n", value);
    printf("Double: %d\n", value * 2);

    /* C Deep Dive: scanf is error-prone */
    /* Auto provides safer input alternatives */
    printf("Auto provides safe input parsing\n");

    return 0;
}
