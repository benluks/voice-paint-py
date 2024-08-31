#include "analysis.h"

struct LinpredFormantSolver
{
    LinpredFormantSolver()
        : formantSolver(std::make_shared<Analysis::Formant::FilteredLP>()),
          linpredSolver(std::make_shared<Analysis::LP::Burg>()),
          mResamplerLPC(0),
          mLastSample(0.0)
    {
    }

    std::shared_ptr<Analysis::Formant::FilteredLP> formantSolver;
    std::shared_ptr<Analysis::LP::Burg> linpredSolver;
    Analysis::Resampler mResamplerLPC;
    double mLastSample;
};

Analysis::FormantResult formantResultFromWaveform(std::vector<double> data, double sampleRate)
{
    constexpr double preemphFrequency = 200.0;
    const double preemphFactor = exp(-(2.0 * M_PI * preemphFrequency) / sampleRate);

    if (mWindow.size() != data.size())
    {
        mWindow = Analysis::gaussianWindow((int)data.size(), 2.5);
    }

    constexpr double fsLPC = 11000;
    mResamplerLPC.setRate(sampleRate, fsLPC);

    auto data2 = data;
    for (int i = (int)data.size() - 1; i >= 1; --i)
    {
        data2[i] = mWindow[i] * (data2[i] - preemphFactor * data2[i - 1]);
    }
    data2[0] = mWindow[0] * (data[0] - preemphFactor * mLastSample);
    mLastSample = data[0];

    auto mLPC = mResamplerLPC.process(data2);

    std::vector<double> lpc;

    double gain;
    lpc = mLinpredSolver->solve(mLPC.data(), (int)mLPC.size(), 10, &gain);
    auto formantResult = mFormantSolver->solve(lpc.data(), (int)lpc.size(), fsLPC);
};