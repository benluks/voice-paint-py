# setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import (
    build_ext,
)  # Import build_ext from pybind11's setup_helpers
import pybind11
import numpy

# Define the extension module
ext_modules = [
    Extension(
        "analysis",  # The name of the module
        [
            "bindings.cpp",
            "fft/realfft.cpp",
            "fft/wisdom.cpp",
            "formant/filteredlp.cpp",
            "linpred/burg.cpp",
            "pitch/mpm.cpp",
            "util/parabolic_interpolation.cpp",
            "util/aberth.cpp",
            "util/calc_formant.cpp",
            "util/eval_polynomial.cpp",
            "util/find_roots.cpp",
            "util/gaussian_window.cpp",
            "util/resampler.cpp",
            "util/sort_formants.cpp",
        ],  # List all C++ source files
        include_dirs=[
            pybind11.get_include(),  # Include pybind11 headers
            numpy.get_include(),  # Include NumPy headers
            "./fft",
            "./formant",
            "./linpred",
            "./pitch",
            "./util",
            "/usr/local/include",
            # "/usr/local/include/samplerate.h"
        ],
        library_dirs=[
            "/usr/local/lib",
            # "/usr/local/lib/libsamplerate.dylib"
        ],
        libraries=["fftw3", "samplerate"],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
]

# Configure the setup
setup(
    name="analysis",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},  # Use pybind11's build_ext
)
