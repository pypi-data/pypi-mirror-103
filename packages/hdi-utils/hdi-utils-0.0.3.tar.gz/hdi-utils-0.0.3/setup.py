# General utily functions for HDI data parsing
# Developer: Joshua M. Hess, BSc
# Developed at the Vaccine & Immunotherapy Center, Mass. General Hospital

# Import setuptools
import setuptools

# Get the readme
def readme():
    with open("README.md", encoding="UTF-8") as readme_file:
        return readme_file.read()

# Pip configuration
configuration = {
    "name": "hdi-utils",
    "version": "0.0.3",
    "description": "High-dimensional image data utilities",
    "long_description": readme(),
    "long_description_content_type": "text/markdown",
    "classifiers": [
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    "keywords": "high-dimensional image imaging mulitplex",
    "url": "https://github.com/JoshuaHess12/hdi-utils",
    "maintainer": "Joshua Hess",
    "maintainer_email": "joshmhess12@gmail.com",
    "license": "MIT",
    "package_dir": {"": "src"},
    "packages": setuptools.find_packages(where='src'),
    "install_requires":[
              'numpy>=1.20.2',
              'pandas>=1.2.4',
              'pyimzML>=1.4.1',
              'nibabel>=3.2.1',
              'h5py>=3.2.1',
              'scikit-image>=0.18.1',
              'scipy>=1.6.2'
          ]
}

# Apply setup
setuptools.setup(**configuration)
