// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "main.expected.h"

struct Command Command_new(const char* name) {
    struct Command cmd;
    cmd.name = name;
    memset(cmd.args, 0, sizeof(cmd.args));
    cmd.argc = 0;
    return cmd;
}

int main(void) {
    struct Command cmd = Command_new("echo");
    printf("%s %s\n", "Command:", cmd.name);
    printf("%s\n", "Mini shell would fork/exec in C");
    printf("%s\n", "Auto uses higher-level process API");
    return 0;
}
