#include <pybind11/pybind11.h>
#include <pybind11/numpy.h> // For handling NumPy arrays
#include <pybind11/stl.h>
#include <memory>
#include <vector>

#include "analysis.h"

namespace py = pybind11;

PYBIND11_MODULE(analysis, m)
{
    m.doc() = "Python bindings for the analysis project";

    // Expose PitchResult structure
    py::class_<Analysis::PitchResult>(m, "PitchResult")
        .def_readonly("pitch", &Analysis::PitchResult::pitch)
        .def_readonly("voiced", &Analysis::PitchResult::voiced);

    // Expose PitchSolver abstract class
    py::class_<Analysis::PitchSolver, std::shared_ptr<Analysis::PitchSolver>>(m, "PitchSolver")
        .def("solve", &Analysis::PitchSolver::solve); // Bind the pure virtual function

    // Expose MPM class
    py::class_<Analysis::Pitch::MPM, Analysis::PitchSolver, std::shared_ptr<Analysis::Pitch::MPM>>(m, "MPM")
        .def(py::init<>()) // Default constructor
        .def("solve", [](Analysis::Pitch::MPM &self, py::array_t<double> data, int sample_rate)
             {
            // Convert NumPy array to a C++ pointer and size
            py::buffer_info buf = data.request();
            if (buf.ndim != 1) {
                throw std::runtime_error("Input should be a 1D array.");
            }

            double* ptr = static_cast<double*>(buf.ptr);
            int length = static_cast<int>(buf.shape[0]);

            // Call the solve method
            return self.solve(ptr, length, sample_rate); }, "Compute pitch from raw audio signal", py::arg("data"), py::arg("sample_rate"));

    // formants and LP

    // Expose FormantData structure
    py::class_<Analysis::FormantData>(m, "FormantData")
        .def_readonly("frequency", &Analysis::FormantData::frequency)
        .def_readonly("bandwidth", &Analysis::FormantData::bandwidth);

    // Expose FormantResult structure
    py::class_<Analysis::FormantResult>(m, "FormantResult")
        .def_property_readonly("formants", [](const Analysis::FormantResult &self)
                               { return self.formants; });

    // Expose the Formants processor class
    py::class_<Analysis::Processors::Formants>(m, "Formants")
        .def(py::init<>()) // Updated constructor
        .def("processData", [](Analysis::Processors::Formants &self, py::array_t<double> data, double sampleRate)
             {
        // Convert NumPy array to a C++ vector
        py::buffer_info buf = data.request();
        if (buf.ndim != 1)
        {
            throw std::runtime_error("Input should be a 1D array.");
        }

        const double *ptr = static_cast<double *>(buf.ptr);
        std::vector<double> data_vec(ptr, ptr + buf.shape[0]);

        // Call the processData method and get the FormantResult
        return self.processData(data_vec, sampleRate); }, "Process data to extract formants", py::arg("data"), py::arg("sampleRate"));
}
