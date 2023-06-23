#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define Modulo(X, Y) ((unsigned long long)X & ((unsigned long long)Y - 1)) // X % Y, (Y == 2^n)
#include <cstdlib>
#include <memory.h>
#include <cstdio>
typedef unsigned char ui8;
typedef unsigned int ui32;
typedef unsigned long long ui64;
typedef const char *_str;

namespace pyc
{
    template <typename Key, typename Value>
    class Namespace
    {
    public:
        struct keyAndValue
        {
            Key key;
            Value value;
        };
        struct bucket
        {
            unsigned int infobyte;
            keyAndValue space[32];
        };
        bucket *table;
        ui64 table_size;

    public:
        inline auto resize(void) -> void;
        auto find(const Key &) -> Value *;
        auto insert(const Key &, const Value &) -> Value &;

    public:
        Namespace(void);
        ~Namespace(void);
        auto operator[](const Key &) -> Value &;
    };
}

template <typename Key, typename Value>
pyc::Namespace<Key, Value>::Namespace()
    : table(nullptr), table_size(0)
{
}

template <typename Key, typename Value>
pyc::Namespace<Key, Value>::~Namespace()
{
    if (table)
    {
        for (ui64 i = 0; i < table_size; i++)
            for (ui32 j = 1, k = 0; j; j <<= 1, k++)
                if (table[i].infobyte & j)
                    table[i].space[k].key.~Key(), table[i].space[k].value.~Value();
        free(table);
    }
}

template <typename Key, typename Value>
inline auto pyc::Namespace<Key, Value>::resize(void) -> void
{
    if (table_size == 0)
    {
        table_size = 1, table = (bucket *)memset(malloc(sizeof(bucket)), 0, sizeof(bucket));
        return;
    }
    bucket *ptr = table;
    ui64 _size = sizeof(bucket) * (this->table_size <<= 4);
    table = (bucket *)memset(malloc(_size), 0, _size);
    for (ui64 i = 0; i < table_size >> 4; i++)
        for (ui32 j = 1, k = 0; j; j <<= 1, k++)
            if (ptr[i].infobyte & j)
                insert(ptr[i].space[k].key, ptr[i].space[k].value);
    free(ptr);
}

template <typename Key, typename Value>
auto pyc::Namespace<Key, Value>::find(const Key &key) -> Value *
{
    if (!this->table_size)
        return nullptr;
    ui32 bit_idx = 1, idx = 0;
    bucket &b = table[Modulo(key.hash(), table_size)];
    if (!b.infobyte)
        return nullptr;
    while (bit_idx)
    {
        if ((bit_idx & b.infobyte) && b.space[idx].key == key)
            return &(b.space[idx].value);
        bit_idx <<= 1, idx++;
    }
    return nullptr;
}

template <typename Key, typename Value>
auto pyc::Namespace<Key, Value>::insert(const Key &key, const Value &value) -> Value &
{
    if (!table_size)
        resize();
INSERT_BEGIN:
    ui32 bit_idx = 1, idx = 0;
    bucket &b = table[Modulo(key.hash(), table_size)];
    while (bit_idx & b.infobyte)
        bit_idx <<= 1, idx++;
    if (!bit_idx)
    {
        resize();
        // code.1
        goto INSERT_BEGIN;

        /* code.2
        return insert(key, value);
        */
    }
    b.infobyte |= bit_idx;
    b.space[idx].key = key;
    return (b.space[idx].value = value);
}

template <typename Key, typename Value>
auto pyc::Namespace<Key, Value>::operator[](const Key &key) -> Value &
{
    Value *ptr;
    if ((ptr = find(key)))
        return *ptr;
    return insert(key, Value());
}

#endif