// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-03-05.h"

struct Stack Stack_new(void) {
    struct Stack s;
    memset(s.items, 0, sizeof(s.items));
    s.top = 0;
    return s;
}

void Stack_push(struct Stack* s, int val) {
    s->items[s->top] = val;
    s->top = s->top + 1;
}

int Stack_pop(struct Stack* s) {
    s->top = s->top - 1;
    return s->items[s->top];
}

int main(void) {
    struct Stack s = Stack_new();
    Stack_push(&s, 10);
    Stack_push(&s, 20);
    Stack_push(&s, 30);
    printf("%s %d\n", "Popped:", Stack_pop(&s));
    printf("%s %d\n", "Popped:", Stack_pop(&s));
    printf("%s %d\n", "Top:", s.top);
    return 0;
}
