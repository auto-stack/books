// Auto → C transpiled by a2c
#ifndef LISTING_05_05_H
#define LISTING_05_05_H

struct Counter {
    int count;
};

struct Counter Counter_new(void);
void Counter_increment(struct Counter* c);
int Counter_value(struct Counter* c);

#endif
