#include <stdlib.h>

const char *odd_or_even(const int *arr, size_t n)
{
    int sum = 0;

    for (size_t i = 0; i < n; i++) sum += arr[i];

    return sum % 2 == 0 ? "even" : "odd";
}
