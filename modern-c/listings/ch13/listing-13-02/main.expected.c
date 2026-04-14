// Auto -> C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "main.expected.h"

struct Config Config_default(void) {
    struct Config c;
    snprintf(c.name, sizeof(c.name), "unnamed");
    c.value = 0;
    c.active = false;
    return c;
}

struct Config Config_with_name(const char *name) {
    struct Config c;
    snprintf(c.name, sizeof(c.name), "%s", name);
    c.value = 0;
    c.active = true;
    return c;
}

int main(void) {
    struct Config default_cfg = Config_default();
    struct Config named_cfg = Config_with_name("production");
    printf("Default: %s %s\n", default_cfg.name,
           default_cfg.active ? "true" : "false");
    printf("Named: %s %s\n", named_cfg.name,
           named_cfg.active ? "true" : "false");

    return 0;
}
