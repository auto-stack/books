// C
#include <stdio.h>
#include <stdlib.h>

int main() {
    setenv("AUTO_GREETING", "Hello from Auto", 1);

    const char *val = getenv("AUTO_GREETING");
    printf("Greeting: %s\n", val ? val : "default");

    const char *missing = getenv("NONEXISTENT_VAR");
    printf("Missing: %s\n", missing ? missing : "not set");
    return 0;
}
