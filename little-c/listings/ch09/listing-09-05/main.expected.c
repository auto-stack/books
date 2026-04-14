// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-09-05.h"

struct Project Project_new(const char *name, const char *ver, const char *author) {
    return (struct Project){.name = (char *)name, .version = (char *)ver, .author = (char *)author};
}

void Project_info(struct Project p) {
    printf("%s %s\n", "Project:", p.name);
    printf("%s %s\n", "Version:", p.version);
    printf("%s %s\n", "Author:", p.author);
}

int main(void) {
    struct Project p = Project_new("my-project", "0.1.0", "You");
    Project_info(p);
    printf("%s\n", "Now customize this template!");
    printf("%s\n", "Add your own types, functions, and logic.");
    return 0;
}
