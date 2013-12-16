from distutils.core import setup

setup(
    name='Portfolio',
    version='0.1',
    author='Gouthaman Balaraman',
    packages=['Portfolio'],
    url='https://github.com/gouthambs/portfolio',
    license='LICENSE',
    description='A framework for portfolio analysis using python',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas >= 0.12.0",
        "numpy >= 1.8.0",
    ],
)
