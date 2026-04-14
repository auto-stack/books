// Auto → C transpiled by a2c
#include <stdio.h>
#include "listing-03-03.h"

void make_user(int id, float score) {
    UserId uid = (UserId)id;
    Score s = (Score)score;
    printf("%s %d\n", "User ID:", uid);
    printf("%s %f\n", "Score:", s);
}

int main(void) {
    make_user(1, 95.5f);
    return 0;
}
