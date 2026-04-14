// Auto → C transpiled by a2c
#ifndef LISTING_03_04_H
#define LISTING_03_04_H

struct Node {
    int value;
    struct Node* next;
};

struct Node new_node(int val);
void print_list(struct Node* head);

#endif
