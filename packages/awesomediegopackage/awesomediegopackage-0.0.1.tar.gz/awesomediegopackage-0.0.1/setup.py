from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first (useless) package'
LONG_DESCRIPTION = 'My first (useless) package containing some basic (useless) functions that we can use to test whether it use installed correctly.'

# Setting up
setup(
    name="awesomediegopackage",
    version=VERSION,
    author="Diego Stucchi (test)",
    author_email="stucchidiego1994@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'first package'],
    url='https://github.com/DiegoStucchi/DiegosFirstPackageGit',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
