#include "Library/Namespace.hpp"
#include "Library/Identifier.hpp"
#include <iostream>
#include <time.h>
#include <unordered_map>
using namespace std;

auto main(void) -> int
{
    unordered_map<int, int> m;

    clock_t s = clock();
    string str;
    for (int i = 0; i < 100000; i++)
    {
        str += 'a';
        identifier ident(&str[0]);
        ident.hash();
    }
    cout << float(clock() - s) / CLOCKS_PER_SEC << '\n';

    return 0;
}