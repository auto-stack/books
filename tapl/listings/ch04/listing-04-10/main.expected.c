// C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char name[32];
    int age;
} Person;

int cmp_age(const void *a, const void *b) {
    return ((Person*)a)->age - ((Person*)b)->age;
}

int main() {
    Person people[] = {{"Zoe", 25}, {"Al", 60}, {"John", 1}};
    int n = 3;

    printf("Sorted by age:\n");
    qsort(people, n, sizeof(Person), cmp_age);
    for (int i = 0; i < n; i++) {
        printf("  %s (%d)\n", people[i].name, people[i].age);
    }
    return 0;
}
