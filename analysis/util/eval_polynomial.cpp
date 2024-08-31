#include "util.h"

void Analysis::evaluatePolynomialWithDerivative(const std::vector<double> &poly, const double x, double *y, double *dy)
{
    double p = poly[poly.size() - 1];
    double dp = 0.0;

    for (int i = (int)poly.size() - 2; i >= 0; --i)
    {
        dp = dp * x + p;
        p = p * x + poly[i];
    }

    *y = p;
    *dy = dp;
}

void Analysis::evaluatePolynomialWithDerivative(const std::vector<double> &poly, const std::complex<double> &z, std::complex<double> *y, std::complex<double> *dy)
{
    std::complex<double> p = poly[poly.size() - 1];
    std::complex<double> dp = 0.0;

    for (int i = (int)poly.size() - 2; i >= 0; --i)
    {
        dp = dp * z + p;
        p = p * z + poly[i];
    }

    *y = p;
    *dy = dp;
}