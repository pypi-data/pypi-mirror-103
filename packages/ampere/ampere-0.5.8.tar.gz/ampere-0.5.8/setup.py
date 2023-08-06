import setuptools
import numpy

from distutils.command import build_ext
from setuptools import setup, Extension


USE_CYTHON = False

# ext = '.pyx'#  if USE_CYTHON else '.c'
ext = '.c'

ida_dir = "ampere/models/ida"
ida_files = ['ida.c', 'ida_band.c', 'ida_dense.c', 'ida_direct.c', 'ida_ic.c', 'ida_io.c', 'nvector_serial.c', 'sundials_band.c', 'sundials_dense.c', 'sundials_direct.c', 'sundials_math.c', 'sundials_nvector.c']
ida_requirements1 = [ida_dir + '/' + ida_file for ida_file in ida_files]


extensions = [
    Extension("ampere.models.P2D.P2D_fd", [f"ampere/models/P2D/P2D_fd{ext}", *ida_requirements1], include_dirs=['ampere/models/P2D/', numpy.get_include()]),
    Extension("ampere.models.SPM.SPM_fd", [f"ampere/models/SPM/SPM_fd{ext}", *ida_requirements1], include_dirs=[numpy.get_include()]),
    Extension("ampere.models.SPM.SPM_fd_sei", [f"ampere/models/SPM/SPM_fd_sei{ext}", *ida_requirements1], include_dirs=[numpy.get_include()]),
    Extension("ampere.models.SPM.SPM_par", [f"ampere/models/SPM/SPM_par{ext}", *ida_requirements1], include_dirs=[numpy.get_include()]),
]

# if USE_CYTHON:
# from Cython.Build import cythonize
# # # from Cython.Build import new_build_ext as build_ext
# extensions = cythonize(extensions, compiler_directives={'language_level': "3"})

with open("README.md", "r") as fh:
    long_description = fh.read()

# cmdclass = {'build_ext': build_ext}
# print()
print(setuptools.find_packages())
setup(
    name="ampere",
    version="0.5.8",
    author="Neal Dawson-Elli",
    author_email="nealde@uw.edu",
    description="A Python package for working with battery discharge data and physics-based battery models",

    # cmdclass=cmdclass,
    ext_modules=extensions,


    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nealde/Ampere",
    packages=[*setuptools.find_packages()],
    package_data={
        'ampere.models.P2D': ['ampere/models/P2D/*.c'],
        'ampere.models.SPM': ['ampere/models/SPM/*.c']
    },
    # include_package_data=True,
    install_requires=['cython', 'matplotlib < 3.4', 'numpy', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Cython',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords="battery numerical simulation modeling",
)
