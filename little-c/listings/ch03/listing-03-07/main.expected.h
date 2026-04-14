// Auto → C transpiled by a2c
#ifndef LISTING_03_07_H
#define LISTING_03_07_H

struct Book {
    char title[256];
    char author[256];
    int available;
};

struct Book Book_new(const char* title, const char* author);
void Book_borrow(struct Book* b);
void Book_return_book(struct Book* b);

#endif
