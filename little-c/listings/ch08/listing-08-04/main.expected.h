// Auto → C transpiled by a2c
#ifndef LISTING_08_04_H
#define LISTING_08_04_H

struct Config {
    char *name;
    char *version;
    int debug;
};

struct Config Config_new(const char *name, const char *ver);
void Config_display(struct Config c);

#endif
