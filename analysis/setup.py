# setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import build_ext  # Import build_ext from pybind11's setup_helpers
import pybind11
import numpy

# Define the extension module
ext_modules = [
    Extension(
        'analysis',  # The name of the module
        [
            'bindings.cpp',
            'pitch/mpm.cpp',
            # 'fft/complexfft.cpp',
            # 'fft/fft_n.cpp',
            'fft/realfft.cpp',
            # 'fft/realrealfft.cpp',
            'fft/wisdom.cpp',
            'util/parabolic_interpolation.cpp'
            ],  # List all C++ source files
        include_dirs=[
            pybind11.get_include(),  # Include pybind11 headers
            numpy.get_include(),     # Include NumPy headers
            './fft',                 # Path to fft headers
            './pitch',               # Path to pitch headers
            './util',                # Path to util headers
             '/usr/local/include',    # Path to FFTW headers
        ],
        library_dirs=[
            '/usr/local/lib',        # Path to FFTW libraries
        ],
        libraries=['fftw3'], 
        language='c++',
        extra_compile_args=['-std=c++11'],  # Ensure C++11 standard
    ),
]

# Configure the setup
setup(
    name='analysis',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},  # Use pybind11's build_ext
)
