#include "util.h"
// #include "laguerre.h"
#include "aberth.h"
#include <iostream>

std::vector<std::complex<double>> Analysis::findRoots(const std::vector<double>& p)
{
    auto roots = Analysis::aberthRoots(p);
    return roots;
}

