// Auto → C transpiled by a2c
#include <stdio.h>

const char* day_type(int day) {
    switch (day) {
        case 1: return "Monday";
        case 2: return "Tuesday";
        case 3: return "Wednesday";
        case 4: return "Thursday";
        case 5: return "Friday";
        case 6: return "Weekend";
        case 7: return "Weekend";
        default: return "Invalid";
    }
}

int main(void) {
    for (int d = 1; d < 8; d++) {
        printf("%s %d %s %s\n", "Day", d, "is", day_type(d));
    }
    return 0;
}
