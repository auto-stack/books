// C
#include <stdio.h>
#include <string.h>

// Note: C does not have built-in JSON. This is a conceptual equivalent.
// In practice, you would use a library like cJSON or jansson.

typedef struct {
    char name[64];
    int age;
} User;

int main() {
    User alice = { .name = "Alice", .age = 30 };
    printf("{\"name\":\"%s\",\"age\":%d}\n", alice.name, alice.age);
    printf("Alice\n");
    printf("30\n");

    User bob = { .name = "Bob", .age = 25 };
    printf("[{\"name\":\"%s\",\"age\":%d},{\"name\":\"%s\",\"age\":%d}]\n",
           alice.name, alice.age, bob.name, bob.age);
    return 0;
}
