#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define LBITSHIFT(X) ((X << 1) + 1)
#define RBITSHIFT(X) ((unsigned long long)X >> 1)
#define Modulo(X, Y) (X & Y) // X % Y (Y == 2^n - 1)
#include <vector>
using namespace std;
typedef unsigned long long ull;

template <typename Type>
class Namespace
{
private:
    struct node
    {
        ull key;
        Type
    };

    vector<node *> table;

public:
    Namespace();
    auto operator[](const ull) -> Type &;
};

#endif