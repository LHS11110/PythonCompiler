#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define Modulo(X, Y) (X & (Y - 1)) // X % Y, (Y == 2^n)
#include <cstdlib>
using namespace std;
typedef unsigned long long ull;

namespace pyc
{
    template <typename Type>
    class Namespace
    {
    public:
        struct bucket
        {
            unsigned int infobyte;
            Type space[32];
        };
        bucket *table;
        unsigned int table_size;

    private:
        auto hash(const unsigned char *) -> unsigned int;
        inline auto resize(void) -> void;

    public:
        Namespace(void);
    };
}

#endif