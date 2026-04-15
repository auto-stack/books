// C
#include <stdio.h>
#include <stdbool.h>
#include <time.h>

int main(void) {
    time_t now = time(NULL);
    printf("%s", ctime(&now));

    struct tm* tm_now = localtime(&now);
    char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", tm_now);
    printf("%s\n", buf);

    struct tm parsed = {0};
    strptime("2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S", &parsed);
    mktime(&parsed);
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &parsed);
    printf("%s\n", buf);

    int total_sec = 2 * 3600 + 30 * 60;
    printf("%dh %dm\n", total_sec / 3600, (total_sec % 3600) / 60);

    time_t later = now + total_sec;
    printf("%s", ctime(&later));

    int diff_min = (int)(difftime(later, now) / 60);
    printf("%d\n", diff_min);
    return 0;
}
