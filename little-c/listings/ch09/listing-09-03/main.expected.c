// Auto → C transpiled by a2c
#include <stdio.h>
#include <string.h>
#include "listing-09-03.h"

struct Response handle_request(struct Request req) {
    if (strcmp(req.path, "/") == 0) {
        return (struct Response){.status = 200, .body = "Welcome!"};
    } else if (strcmp(req.path, "/about") == 0) {
        return (struct Response){.status = 200, .body = "About page"};
    } else {
        return (struct Response){.status = 404, .body = "Not found"};
    }
}

int main(void) {
    struct Request req = (struct Request){.method = "GET", .path = "/"};
    struct Response res = handle_request(req);
    printf("%s %d\n", "Status:", res.status);
    printf("%s %s\n", "Body:", res.body);
    return 0;
}
