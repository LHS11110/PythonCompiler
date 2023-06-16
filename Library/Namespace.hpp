#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define Modulo(X, Y) (X & (Y - 1)) // X % Y, (Y == 2^n)
#include <cstdlib>
#include <memory.h>
using namespace std;
typedef unsigned char ui8;
typedef unsigned int ui32;
typedef unsigned long long ui64;
typedef const char *_str;

namespace pyc
{
    template <typename Type>
    class Namespace
    {
    private:
        struct bucket
        {
            struct keyAndValue
            {
                _str key;
                Type value;
            };
            unsigned int infobyte;
            keyAndValue space[32];
        };
        bucket *table;
        unsigned int table_size;

    private:
        // Jenkins hash function
        inline auto hash(_str) -> ui32;
        inline auto resize(void) -> void;
        auto find(_str, ui32) -> Type *;

    public:
        Namespace(void);
        auto find(_str) -> Type *;
    };
}

template <typename Type>
pyc::Namespace<Type>::Namespace()
    : table(nullptr), table_size(0)
{
}

template <typename Type>
inline auto pyc::Namespace<Type>::hash(_str key) -> ui32
{
    int c = 0;
    ui32 hash = 0;
    while ((c = *(const unsigned char *)key++))
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

template <typename Type>
inline auto pyc::Namespace<Type>::resize(void) -> void
{
    if (this->table_size == 0)
    {
        this->table_size = 1, this->table = memset(malloc(sizeof(bucket)), 0, sizeof(bucket));
        return;
    }
    bucket *ptr = this->table;
    ui64 _size = sizeof(bucket) * (this->table_size <<= 1);
    this->table = memcpy(memset(malloc(_size), 0, _size), this->table, _size >> 1);
    free(ptr);
}

template <typename Type>
auto pyc::Namespace<Type>::find(_str key) -> Type *
{
    if (!this->table_size)
        return nullptr;
    ui32 bit_idx = 1, idx = 0;
    bucket &b = this->table[Modulo(hash(key), this->table_size)];
    if (!b.infobyte)
        return nullptr;
    while (bit_idx)
    {
        if ((bit_idx & b.infobyte) && !strcmp(b.space[idx].key, key))
            return b.space[idx].value;
        bit_idx <<= 1, idx++;
    }
    return nullptr;
}

template <typename Type>
auto pyc::Namespace<Type>::find(_str key, ui32 hash_value) -> Type *
{
    if (!this->table_size)
        return nullptr;
    ui32 bit_idx = 1, idx = 0;
    bucket &b = this->table[Modulo(hash_value, this->table_size)];
    if (!b.infobyte)
        return nullptr;
    while (bit_idx)
    {
        if ((bit_idx & b.infobyte) && !strcmp(b.space[idx].key, key))
            return b.space[idx].value;
        bit_idx <<= 1, idx++;
    }
    return nullptr;
}

#endif