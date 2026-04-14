// Auto → C transpiled by a2c
#include <stdio.h>
#include <stdlib.h>
#include "listing-03-04.h"

struct Node new_node(int val) {
    struct Node n = (struct Node){.value = val, .next = NULL};
    return n;
}

void print_list(struct Node* head) {
    struct Node* current = head;
    while (current != NULL) {
        printf("%d\n", current->value);
        current = current->next;
    }
}

int main(void) {
    struct Node a = new_node(1);
    struct Node b = new_node(2);
    struct Node c = new_node(3);
    a.next = &b;
    b.next = &c;
    printf("%s\n", "Linked list:");
    print_list(&a);
    return 0;
}
