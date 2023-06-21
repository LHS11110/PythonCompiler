#ifndef _IDENTIFIER_HPP
#define _IDENTIFIER_HPP
#include <cstring>

class identifier
{
private:
    const char *str;
    unsigned long long len;

public:
    identifier();
    identifier(const char *_str);

    auto hash() -> unsigned int;
};

#endif