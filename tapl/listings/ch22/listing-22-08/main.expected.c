// C
#include <stdio.h>
#include <string.h>

int main() {
    const char *query = "name=hello&age=20";
    printf("Query string: %s\n", query);

    int pair_count = 0;
    char q[64];
    strncpy(q, query, 64);
    char *token = strtok(q, "&");
    while (token != NULL) {
        pair_count++;
        token = strtok(NULL, "&");
    }
    printf("Parameter count: %d\n", pair_count);
    return 0;
}
