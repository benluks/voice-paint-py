#ifndef ANALYSIS_PROCESSOR_FORMANTS_H
#define ANALYSIS_PROCESSOR_FORMANTS_H

#include <memory>

#include "../util/util.h" // for resampler
#include "../formant/formant.h"
#include "../linpred/linpred.h"

namespace Analysis::Processors
{

    class Formants
    {
    public:
        Formants();

        Analysis::FormantResult processData(const std::vector<double> &data, double sampleRate);

    private:
    
        double mTime;

        std::vector<double> mData;

        // from `processors/formants/formants.h`
        std::shared_ptr<Analysis::LinpredSolver> mLinpredSolver;
        std::shared_ptr<Analysis::FormantSolver> mFormantSolver;

        std::vector<double> mWindow;
        Analysis::Resampler mResamplerLPC;

        double mLastSample;
    };

}

#endif // PIPELINE_PROCESSOR_FORMANTS_H