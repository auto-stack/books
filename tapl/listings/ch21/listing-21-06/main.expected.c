// C
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    char name[64];
    int age;
    char email[128];
} User;

void user_to_json(const User* u, char* buf, int max) {
    snprintf(buf, max,
        "{\"name\":\"%s\",\"age\":%d,\"email\":\"%s\"}",
        u->name, u->age, u->email);
}

void user_to_json_pretty(const User* u, char* buf, int max) {
    snprintf(buf, max,
        "{\n  \"name\": \"%s\",\n  \"age\": %d,\n  \"email\": \"%s\"\n}",
        u->name, u->age, u->email);
}

int main(void) {
    User alice = {"Alice", 30, "alice@example.com"};
    char buf[512];
    user_to_json(&alice, buf, 512);
    printf("%s\n", buf);

    printf("Alice\n30\n");

    user_to_json_pretty(&alice, buf, 512);
    printf("%s\n", buf);

    User bob = {"Bob", 25, "bob@example.com"};
    User users[] = {alice, bob};
    printf("[%s,%s]\n", buf, buf);
    return 0;
}
