// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-03-07.h"

struct Book Book_new(const char* title, const char* author) {
    struct Book b;
    strncpy(b.title, title, sizeof(b.title) - 1);
    b.title[sizeof(b.title) - 1] = '\0';
    strncpy(b.author, author, sizeof(b.author) - 1);
    b.author[sizeof(b.author) - 1] = '\0';
    b.available = 1;
    return b;
}

void Book_borrow(struct Book* b) {
    if (b->available) {
        b->available = 0;
        printf("%s %s\n", "Borrowed:", b->title);
    } else {
        printf("%s %s\n", "Not available:", b->title);
    }
}

void Book_return_book(struct Book* b) {
    b->available = 1;
    printf("%s %s\n", "Returned:", b->title);
}

int main(void) {
    struct Book b1 = Book_new("The C Programming Language", "K&R");
    struct Book b2 = Book_new("Auto Programming", "Auto Team");
    Book_borrow(&b1);
    Book_borrow(&b1);
    Book_return_book(&b1);
    Book_borrow(&b1);
    return 0;
}
