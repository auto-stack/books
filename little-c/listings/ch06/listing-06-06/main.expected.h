// Auto → C transpiled by a2c
#ifndef MAIN_EXPECTED_H
#define MAIN_EXPECTED_H

struct Command {
    const char* name;
    const char* args[10];
    int argc;
};

struct Command Command_new(const char* name);

#endif /* MAIN_EXPECTED_H */
