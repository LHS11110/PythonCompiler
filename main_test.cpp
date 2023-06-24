#include "Library/Namespace.hpp"
#include <iostream>
#include <time.h>
#include <unordered_map>
using namespace std;

class integer
{
private:
    int num;

public:
    integer()
        : num(0)
    {
    }

    integer(const int n)
        : num(n)
    {
    }

    inline unsigned int hash() const
    {
        return num;
    }

    inline bool operator==(const integer &t) const
    {
        return t.num == num;
    }

    ~integer()
    {
    }
};

auto main(void) -> int
{
    pyc::Namespace<integer, int> m;
    clock_t s = clock();
    for (int i = 0; i < 10000000; i++)
        m[i] = i;
    std::cout << ((float)(clock() - s) / 1000000) << '\n';
    std::cout << m.table_size << '\n';
    std::cout << m[34343] << '\n';

    return 0;
}