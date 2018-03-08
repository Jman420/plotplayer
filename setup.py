from setuptools import setup, find_packages

setup(name='plotplayer',
        version='5.4.0',
        description='Function based animation player for Matplotlib',
        long_description=open("Readme.md").read(),
        url='https://github.com/Jman420/plotplayer',
        author='Justin Giannone',
        author_email='jman.giannone@gmail.com',
        license='Apache 2.0',
        packages=find_packages(exclude=['test']),
        zip_safe=False)
