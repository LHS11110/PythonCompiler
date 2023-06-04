#include "Namespace.hpp"

template <typename Type>
Namespace<Type>::Namespace()
    : table(vector<Namespace::node *>())
{
}

template <typename Type>
auto Namespace<Type>::operator[](const ull key) -> Type &
{
    ull _size = table.size();
    node *empty_node = nullptr;
    while (_size)
    {
        _size = RBITSHIFT(_size);
    }
}