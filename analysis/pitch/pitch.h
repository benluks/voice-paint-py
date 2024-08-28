#ifndef ANALYSIS_PITCH_H
#define ANALYSIS_PITCH_H

#include <cstdint>
#include <memory>

#include "../fft/fft.h"
#include "rapt.h"

namespace Analysis {
        
    struct PitchResult {
        double pitch;
        bool voiced;
    };

    class PitchSolver {
    public:
        virtual ~PitchSolver() {}
        virtual PitchResult solve(const double *data, int length, int sampleRate) = 0;
    };

    namespace Pitch {

        class MPM : public PitchSolver {
        public:
            PitchResult solve(const double *data, int length, int sampleRate) override;
        };
        
        class RAPT : public PitchSolver, public Analysis::RAPT {
        public:
            RAPT();
            PitchResult solve(const double *data, int length, int sampleRate) override;
        private:
            std::vector<double> pitches;
        };
    }
}

#endif // ANALYSIS_PITCH_H
