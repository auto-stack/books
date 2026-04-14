// Auto → C transpiled by a2c
#include <stdio.h>
#include <assert.h>

int abs_val(int n) {
    assert(n >= 0 && "abs_val expects non-negative input");
    return n;
}

int max(int a, int b) {
    assert(a >= 0 && b >= 0 && "inputs must be non-negative");
    if (a > b) { return a; } else { return b; }
}

int main(void) {
    printf("%s %d\n", "abs(5) =", abs_val(5));
    printf("%s %d\n", "max(3, 7) =", max(3, 7));
    printf("%s\n", "Assertions catch logic errors early");
    return 0;
}
