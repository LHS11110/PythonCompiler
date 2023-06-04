#include "Namespace.hpp"

inline auto pyc::id() -> ull
{
    static ull _id = 0;
    return _id++;
}

template <typename Type>
pyc::Namespace<Type>::node::node(ull _k, const Type &_v)
    : key(_k), value(_v)
{
}

template <typename Type>
pyc::Namespace<Type>::Namespace()
    : table(vector<Namespace::node *>())
{
}

template <typename Type>
auto pyc::Namespace<Type>::operator[](const ull key) -> Type &
{
    ull idx, empty_idx;
    idx = empty_idx = table.size();
    if (idx)
    {
        ull _mcache = 0;
        node *ptr = nullptr;
        goto find;
        do
        {
            idx >>= 1;
        find:
            if ((ptr = table[_mcache = Modulo(key, idx)]) == nullptr)
            {
                empty_idx = _mcache;
                continue;
            }
            if (ptr->key == key)
                return ptr->value;
        } while (idx);
    }
    if (empty_idx == table.size())
    {
        if (!empty_idx)
            table.resize(1);
        else
            table.resize(empty_idx <<= 1);
        return (table[Modulo(key, empty_idx)] = new node(key, Type()))->value;
    }
    return (table[empty_idx] = new node(key, Type()))->value;
}