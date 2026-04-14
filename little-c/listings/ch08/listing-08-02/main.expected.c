// Auto → C transpiled by a2c
#include <stdio.h>

void worker(int id) {
    printf("%s %d %s\n", "Worker", id, "running");
}

int main(void) {
    printf("%s\n", "Threading in C uses pthreads");
    printf("%s\n", "Auto uses task-based concurrency instead");
    printf("%s\n", "Tasks communicate via mailboxes");
    worker(1);
    worker(2);
    printf("%s\n", "In C, these would run in parallel threads");
    return 0;
}
