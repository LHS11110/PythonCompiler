#include "Namespace.hpp"

template <typename Type>
pyc::Namespace<Type>::Namespace()
    :
{
}

template <typename Type>
auto pyc::Namespace<Type>::hash(const char *key) -> unsigned int
{
    int c = 0;
    unsigned int hash = 0;
    while (c = *key++)
    {
        hash += c;
        hash += hash << 10;
        hash ^= hash >> 6;
    }
    hash += hash << 3;
    hash ^= hash >> 11;
    hash += hash << 15;
    return hash;
}