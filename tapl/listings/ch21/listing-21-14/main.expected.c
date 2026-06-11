// C
#include <stdio.h>
#include <math.h>

int main() {
    double x = 2.0;
    double y = 3.0;

    double power = pow(x, y);
    double sqrt_val = sqrt(x);
    printf("%.1f ^ %.1f = %.1f\n", x, y, power);
    printf("sqrt(%.1f) = %.6f\n", x, sqrt_val);

    double neg = -5.0;
    double abs_result = fabs(neg);
    printf("|%.1f| = %.1f\n", neg, abs_result);

    double pi = 3.14159265;
    double sin_val = sin(pi);
    double cos_val = cos(pi);
    printf("sin(pi) = %.6f\n", sin_val);
    printf("cos(pi) = %.6f\n", cos_val);
    return 0;
}
