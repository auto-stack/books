// Auto → C transpiled by a2c
#ifndef LISTING_09_03_H
#define LISTING_09_03_H

struct Request {
    char *method;
    char *path;
};

struct Response {
    int status;
    char *body;
};

struct Response handle_request(struct Request req);

#endif
