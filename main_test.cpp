#include "Library/Namespace.hpp"
#include <iostream>
using namespace std;

auto main(void) -> int
{
    cout << sizeof(pyc::Namespace<short>::bucket::space) << '\n';
    cout << (8 * 32) << '\n';

    return 0;
}