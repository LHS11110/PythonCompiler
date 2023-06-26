#include "Library/set.hpp"
#include <iostream>
#include <time.h>
#include <unordered_map>
using namespace std;

class integer
{
public:
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
    pyc::set<integer, int> m;
    int e;
    cin >> e;
    clock_t s = clock();
    for (int i = 0; i < e; i++)
        m[i] = i;
    std::cout << ((float)(clock() - s) / CLOCKS_PER_SEC) << '\n';
    std::cout << m.size() << '\n';
    cout << "\n\n";

    return 0;
}