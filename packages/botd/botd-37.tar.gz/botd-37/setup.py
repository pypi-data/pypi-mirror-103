# This file is placed in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botd',
    version='37',
    url='https://github.com/bthate/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="24/7 channel daemon",
    long_description=read(),
    license='Public Domain',
    packages=["botd", "botl"],
    install_requires=["feedparser"],
    zip_safe=True,
    scripts=["bin/botl", "bin/botctl", "bin/botd"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
