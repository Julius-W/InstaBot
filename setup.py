from setuptools import setup, find_packages

setup(
    name='InstaBot',
    version='0.1.0',
    description='A simple library for managing an Instagram bot.',
    url='https://github.com/Julius-W/InstaBot',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['selenium'],
)