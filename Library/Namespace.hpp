#ifndef _NAMESPACE_HPP
#define _NAMESPACE_HPP
#define Modulo(X, Y) ((unsigned long long)X & ((unsigned long long)Y - 1)) // X % Y, (Y == 2^n)
#include <cstdlib>
#include <memory.h>
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
        inline auto find(const Key &) const -> Value *;
        inline auto insert(const Key &, const Value &) -> Value &;

    public:
        Namespace(void);
        ~Namespace(void);
        inline auto operator[](const Key &) -> Value &;
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
    ui64 _size = sizeof(bucket) * (table_size <<= 4);
    table = (bucket *)memset(malloc(_size), 0, _size);
    for (ui64 i = 0; i < table_size >> 4; i++)
        for (ui32 j = 1, k = 0; j; j <<= 1, k++)
            if (ptr[i].infobyte & j)
                insert(ptr[i].space[k].key, ptr[i].space[k].value), ptr[i].space[k].key.~Key(), ptr[i].space[k].value.~Value();
    free(ptr);
}

template <typename Key, typename Value>
inline auto pyc::Namespace<Key, Value>::find(const Key &key) const -> Value *
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
inline auto pyc::Namespace<Key, Value>::insert(const Key &key, const Value &value) -> Value &
{
    if (!table_size)
        resize();
    ui32 bit_idx = 1, idx = 0, hash_value = key.hash();
    bucket *b = &table[Modulo(hash_value, table_size)];
    while (true)
    {
        if (b->infobyte == -1)
        {
            resize();
            // code.1
            bit_idx = 1, idx = 0;
            b = &table[Modulo(hash_value, table_size)];
            continue;

            /* code.2
            return insert(key, value);
            */
        }
        while (bit_idx & b->infobyte)
            bit_idx <<= 1, idx++;
        b->infobyte |= bit_idx;
        b->space[idx].key = key;
        return (b->space[idx].value = value);
    }
}

template <typename Key, typename Value>
inline auto pyc::Namespace<Key, Value>::operator[](const Key &key) -> Value &
{
    if (!table_size)
        resize();
    ui32 bit_idx = 1, idx = 0, hash_value = key.hash();
    bucket *b = &table[Modulo(hash_value, table_size)];
    while (bit_idx)
    {
        if ((bit_idx & b->infobyte) && b->space[idx].key == key)
            return b->space[idx].value;
        bit_idx <<= 1, idx++;
    }
    bit_idx = 1, idx = 0;
    while (true)
    {
        if (b->infobyte == -1)
        {
            resize();
            // code.1
            bit_idx = 1, idx = 0;
            b = &table[Modulo(hash_value, table_size)];
            continue;

            /* code.2
            return insert(key, Value());
            */
        }
        while (bit_idx & b->infobyte)
            bit_idx <<= 1, idx++;
        b->infobyte |= bit_idx;
        b->space[idx].key = key;
        return (b->space[idx].value = Value());
    }
}

#endif