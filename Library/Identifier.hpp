#ifndef _IDENTIFIER_HPP
#define _IDENTIFIER_HPP
#include <cstring>
#include <cstdlib>

class identifier
{
private:
    const char *str;
    unsigned long long len;

public:
    identifier();
    identifier(const char *_str);

    auto hash() const -> unsigned int;
    auto operator==(const identifier &) const -> bool;
};

#endif