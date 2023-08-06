from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'Its not much, but a decent attempt🙂'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="noobcode",
    version=VERSION,
    author="Himanshu",
    author_email="addyjeridiq@email.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
