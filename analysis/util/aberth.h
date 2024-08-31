#ifndef ANALYSIS_UTIL_ABERTH_H
#define ANALYSIS_UTIL_ABERTH_H

#include <complex>

namespace Analysis {

std::vector<std::complex<double>> aberthRoots(const std::vector<double>& P);

std::vector<std::complex<double>> aberthRootsAroundInitial(
        const std::vector<double>& P, double r, double phi, int count);

}

#endif // ANALYSIS_UTIL_ABERTH_H


