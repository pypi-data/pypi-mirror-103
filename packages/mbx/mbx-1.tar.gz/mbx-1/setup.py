# This file is place in the Public Domain.

from setuptools import setup, os

def mods(name):
    res = []
    for p in os.listdir(name):
        if p.endswith(".py"):
           res.append(p[:-3])
    return res

def read():
    return open("README.rst", "r").read()

setup(
    name='mbx',
    version='1',
    description="mailbox scanner",
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    url='https://github.com/bthate67/mbx',
    long_description=read(),
    install_requires=["olib"],
    license='Public Domain',
    scripts=["bin/mbx"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
