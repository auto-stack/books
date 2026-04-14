// Auto → C transpiled by a2c
#ifndef LISTING_03_05_H
#define LISTING_03_05_H

struct Stack {
    int items[100];
    int top;
};

struct Stack Stack_new(void);
void Stack_push(struct Stack* s, int val);
int Stack_pop(struct Stack* s);

#endif
