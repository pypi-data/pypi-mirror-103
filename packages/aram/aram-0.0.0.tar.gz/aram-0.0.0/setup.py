import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(include_package_data=True,
    name="aram",                     # This is the name of the package
    version='',              # The initial release version
    author="Thomas Morris",                     # Full name of the author
    description="Atmospheric Modeling (BETA)",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
    py_modules=["aram",'aram_tools','products'],             # Name of the python package
    package_dir={'':'aram/src'},     # Directory of the source code of the package
    install_requires=['numpy','scipy']                     # Install other dependencies if any

)
