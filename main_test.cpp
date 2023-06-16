#include "Library/Namespace.hpp"
#include <iostream>
#include <time.h>
#include <unordered_map>
using namespace std;

auto main(void) -> int
{
    unordered_map<int, int> m;

    clock_t s = clock();
    for (long long i = 0; i < 500000000; i++)
    {
    }
    cout << float(clock() - s) / CLOCKS_PER_SEC << '\n';

    return 0;
}