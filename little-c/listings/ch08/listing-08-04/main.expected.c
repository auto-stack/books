// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-08-04.h"

struct Config Config_new(const char *name, const char *ver) {
    return (struct Config){.name = (char *)name, .version = (char *)ver, .debug = 0};
}

void Config_display(struct Config c) {
    /* simplified: print name + version */
    printf("%s %s%s%s\n", c.name, "v", c.version, "");
    if (c.debug) {
        printf("%s\n", "  [DEBUG MODE]");
    }
}

int main(void) {
    struct Config cfg = Config_new("myapp", "1.0.0");
    Config_display(cfg);
    return 0;
}
