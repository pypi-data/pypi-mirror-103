import setuptools
import numpy

import os

from distutils.core import setup
from distutils.extension import Extension

try:
    import Cython
except ImportError:
    os.system('pip3 install --upgrade cython setuptools')

from Cython.Distutils import build_ext
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()
ida_dir = "ampere/models/ida"
ida_files = ['ida.c', 'ida_band.c', 'ida_dense.c', 'ida_direct.c', 'ida_ic.c', 'ida_io.c', 'nvector_serial.c', 'sundials_band.c', 'sundials_dense.c', 'sundials_direct.c', 'sundials_math.c', 'sundials_nvector.c']
ida_requirements1 = [ida_dir + '/' + ida_file for ida_file in ida_files]


ext_modules = [
    Extension("ampere.models.P2D.P2D_fd", ["ampere/models/P2D/P2D_fd.pyx", "ampere/models/P2D/P2D_fd.c", *ida_requirements1], include_dirs=[numpy.get_include()]),
    Extension("ampere.models.SPM.SPM_fd", ["ampere/models/SPM/SPM_fd.pyx", "ampere/models/SPM/SPM_fd.c", *ida_requirements1], include_dirs=[numpy.get_include()]),
    Extension("ampere.models.SPM.SPM_fd_sei", ["ampere/models/SPM/SPM_fd_sei.pyx", "ampere/models/SPM/SPM_fd_sei.c", *ida_requirements1], include_dirs=[numpy.get_include()]),
    Extension("ampere.models.SPM.SPM_par", ["ampere/models/SPM/SPM_par.pyx", "ampere/models/SPM/SPM_par.c", *ida_requirements1], include_dirs=[numpy.get_include()]),
]
cmdclass = {'build_ext': build_ext}

print(setuptools.find_packages())
setup(
    name="ampere",
    version="0.5.1",
    author="Neal Dawson-Elli",
    author_email="nealde@uw.edu",
    description="A Python package for working with battery discharge data and physics-based battery models",

    cmdclass=cmdclass,
    ext_modules=cythonize(ext_modules),

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nealde/Ampere",
    packages=[*setuptools.find_packages()],
    install_requires=['cython', 'matplotlib', 'numpy', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Cython',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords="battery numerical simulation modeling",
)
