// C
#include <stdio.h>
#include <string.h>

int main() {
    const char *msg = "hello";
    /* C uses error codes; conceptual equivalent: */
    const char *val = msg;
    printf("Got: %s\n", val);

    /* Error propagation in C would use return codes */
    printf("something went wrong\n");
    return 1;
}
