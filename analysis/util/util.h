#ifndef ANALYSIS_UTIL_H
#define ANALYSIS_UTIL_H

#include <vector>
#include "../formant/formant.h"
#include <samplerate.h>

#include <complex>

namespace Analysis
{

    std::vector<int> findPeaks(const double *data, int length, int sign = +1);

    std::pair<std::vector<double>, std::vector<double>> findZerocros(const std::vector<double> &y, char m);

    std::pair<double, double> parabolicInterpolation(const std::vector<double> &array, int x);

    std::vector<std::complex<double>> findRoots(const std::vector<double> &p);

    FormantData calculateFormant(double r, double phi, double sampleRate);

    void sortFormants(std::vector<FormantData> &formants);

    void polishComplexRoot(const std::vector<double> &p, std::complex<double> *root, int maxIt);
    void polishRealRoot(const std::vector<double> &p, double *root, int maxIt);
    void polishRoots(const std::vector<double> &p, std::vector<std::complex<double>> &roots);

    std::vector<std::complex<double>> evaluatePolynomialComplexVector(const std::vector<double> &poly, const std::vector<std::complex<double>> &x);
    void evaluatePolynomialWithDerivative(const std::vector<double> &p, double x, double *y, double *dy);
    void evaluatePolynomialWithDerivative(const std::vector<double> &p, const std::complex<double> &x, std::complex<double> *y, std::complex<double> *dy);

    std::vector<std::complex<double>> evaluatePolynomialDerivatives(const std::vector<std::complex<double>> &p, const std::complex<double> &x, int numberOfDerivatives);
    std::vector<double> gaussianWindow(int length, double alpha);

    class Resampler
    {
    public:
        static constexpr int chMono = 1;

        Resampler(int inRate = 0);
        Resampler(int inRate, int outRate);
        virtual ~Resampler();

        constexpr int getNumChannels() const { return chMono; }

        void setInputRate(int inRate);
        void setOutputRate(int outRate);
        void setRate(int inRate, int outRate);

        int getInputRate() const;
        int getOutputRate() const;
        void getRate(int *pInRate, int *pOutRate) const;

        int getRequiredInLength(int outLength) const;
        int getExpectedOutLength(int inLength) const;

        std::vector<double> process(const std::vector<double> &in);

    private:
        void updateRatio();
        void setupResampler();

        int mId;

        SRC_STATE *mSrc;
        int mInRate, mOutRate;

        static std::atomic_int sId;
    };

}

#endif // ANALYSIS_UTIL_H
