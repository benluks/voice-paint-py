#ifndef ANALYSIS_FORMANT_H
#define ANALYSIS_FORMANT_H

#include <vector>


namespace Analysis
{

    struct FormantData
    {
        double frequency;
        double bandwidth;
    };

    struct FormantResult
    {
        std::vector<FormantData> formants;
    };

    class FormantSolver
    {
    public:
        virtual FormantResult solve(const double *lpc, int lpcOrder, double sampleRate) = 0;
    };

    namespace Formant
    {
        class FilteredLP : public FormantSolver
        {
        public:
            FormantResult solve(const double *lpc, int lpcOrder, double sampleRate) override;
        };

    };
}

#endif // ANALYSIS_FORMANT_H