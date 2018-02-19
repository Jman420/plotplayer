from setuptools import setup
from setuptools import setuptools

setuptools.setup(name='plotplayer',
                  version='4.0.0',
                  description='Lightweight function based animation player for Matplotlib',
                  url='https://github.com/Jman420/plotplayer',
                  author='Justin Giannone',
                  author_email='jman.giannone@gmail.com',
                  license='Apache 2.0',
                  packages=setuptools.find_packages(exclude=[ "test" ]),
                  zip_safe=False)