#include "Identifier.hpp"

identifier::identifier()
    : str(nullptr), len(0)
{
}

identifier::identifier(const char *_str)
    : str(_str), len(strlen(_str))
{
}