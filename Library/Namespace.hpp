#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define Modulo(X, Y) (X & (Y - 1)) // X % Y, (Y == 2^n)
#include <vector>
using namespace std;
typedef unsigned long long ull;

namespace pyc
{
    template <typename Type>
    class Namespace
    {
    private:
        auto hash(const char *) -> int;

    public:
        Namespace();
    };
}

#endif