#include "util.h"

static inline double G(double x, int L, double alpha)
{
    const int N = L - 1;
    const double k = (x - N / 2.0) / (2 * L * alpha);
    return exp(-(k * k));
}

std::vector<double> Analysis::gaussianWindow(int L, double alpha)
{
    const double Gmh = G(-0.5, L, alpha);
    const double GmhpLpGmhmL = G(-0.5 + L, L, alpha) - G(-0.5 - L, L, alpha);

    std::vector<double> win(L);
    for (int n = 0; n < L; ++n)
    {
        win[n] = G(n, L, alpha) - (Gmh * (G(n + L, L, alpha) + G(n - L, L, alpha))) / GmhpLpGmhmL;
    }
    return win;
}
