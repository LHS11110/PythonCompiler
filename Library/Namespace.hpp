#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define Modulo(X, Y) (X & (Y - 1)) // X % Y (Y == 2^n)
#include <vector>
using namespace std;
typedef unsigned long long ull;

namespace pyc
{
    inline auto id() -> ull;

    template <typename Type>
    class Namespace
    {
    private:
        struct node
        {
            ull key;
            Type value;

            node(ull, const Type &);
        };

        vector<node *> table;

    public:
        Namespace();
        auto operator[](const ull) -> Type &;
    };
}

#endif