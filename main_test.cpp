#include "Library/Namespace.hpp"
#include "Library/Identifier.hpp"
#include <iostream>
#include <time.h>
#include <unordered_map>
using namespace std;

auto main(void) -> int
{
    pyc::Namespace<identifier, int> m;

    clock_t s = clock();
    string str;
    for (int i = 0; i < 10000000; i++)
        m["asd"] = i;
    cout << float(clock() - s) / CLOCKS_PER_SEC << '\n';
    cout << *m.find("asd") << '\n';

    return 0;
}