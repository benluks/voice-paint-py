#include "fft.h"

static const std::vector<double>& getWindow(int N, std::map<int, std::vector<double>>& windowCache) {
    auto wit = windowCache.find(N);
    if (wit == windowCache.end()) {
        constexpr double a0 = 0.35875;
        constexpr double a1 = 0.48829;
        constexpr double a2 = 0.14128;
        constexpr double a3 = 0.01168;
        std::vector<double> w(N);
        for (int j = 0; j < N; ++j) { 
            w[j] = a0 - a1 * cos((2.0 * M_PI * j) / (N - 1))
                        + a2 * cos((4.0 * M_PI * j) / (N - 1))
                        - a3 * cos((6.0 * M_PI * j) / (N - 1));
        }
        windowCache[N] = w;
        return windowCache[N];
    }
    return wit->second;
}

std::vector<double> Analysis::fft_n(Analysis::RealFFT *fft, const std::vector<double>& signal, std::map<int, std::vector<double>>& windowCache)
{
    const int nfft = fft->getInputLength();
    const int n = (int) signal.size();

    if (n <= nfft) {
        for (int i = 0; i < nfft; ++i) {
            fft->input(i) = 0.0;
        }

        auto w = getWindow(n, windowCache);

        for (int j = 0; j < n; ++j) {
            double sample = signal[j];

            fft->input(j) = sample * w[j];
        }
    }
    else {
        auto w = getWindow(nfft, windowCache);

        for (int j = 0; j < nfft; ++j) {
            int i = n / 2 - nfft / 2 + j;
            
            double sample = signal[i];

            fft->input(j) = sample * w[j];
        }
    }

    fft->computeForward();

    std::vector<double> h(fft->getOutputLength());
    for (int k = 0; k < fft->getOutputLength(); ++k) {
        h[k] = std::abs(fft->output(k) * std::conj(fft->output(k)));
    }
    return h;
}
