// Auto → C transpiled by a2c
#ifndef LISTING_09_05_H
#define LISTING_09_05_H

struct Project {
    char *name;
    char *version;
    char *author;
};

struct Project Project_new(const char *name, const char *ver, const char *author);
void Project_info(struct Project p);

#endif
