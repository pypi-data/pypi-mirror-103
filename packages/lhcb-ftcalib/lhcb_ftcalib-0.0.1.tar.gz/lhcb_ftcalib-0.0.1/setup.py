from setuptools import setup

setup(
    name         = "lhcb_ftcalib",
    version      = "0.0.1",
    description  = "Library for calibrating flavour tagging algorithms at LHCb",
    py_modules   = [ "lhcb_ftcalib" ],
    packages     = ["lhcb_ftcalib"],
    license      = "GPLv3",
    package_dir  = {'': 'src'},
    url          = "https://gitlab.cern.ch/lhcb-ft/lhcb_ftcalib",
    author       = "Vukan Jevtic",
    author_email = "vukan.jevtic@cern.ch",
    classifiers  = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
    ],
    install_requires = [
        "numpy",
        "pandas",
        "scipy",
        "iminuit>2.3.0",
        "uncertainties",
        "matplotlib"
    ],
    extras_require = {
        "dev" : [
            "pytest>4"
        ]
    }
)
