#include "Identifier.hpp"

identifier::identifier()
    : str(nullptr), len(0)
{
}

identifier::identifier(const char *_str)
    : str(_str), len(strlen(_str))
{
}

auto identifier::hash() const -> unsigned int
{
    unsigned int hash_value = 0;
    unsigned long long end = len;

    while (end)
    {
        if (end >= 8)
        {
            hash_value += ~*(unsigned long long *)str;
            end -= 8;
        }
        else if (end >= 4)
        {
            hash_value += ~*(unsigned int *)str;
            end -= 4;
        }
        else if (end >= 2)
        {
            hash_value += ~*(unsigned short *)str;
            end -= 2;
        }
        else
        {
            hash_value += ~*(unsigned char *)str;
            end -= 1;
        }
        hash_value += hash_value << 10;
        hash_value ^= hash_value >> 6;
    }

    hash_value += hash_value << 3;
    hash_value ^= hash_value >> 11;
    hash_value += hash_value << 15;

    return hash_value;
}

auto identifier::operator==(const identifier &ident) const -> bool
{
    return !strcmp(str, ident.str);
}