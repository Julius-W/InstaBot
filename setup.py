from setuptools import setup
import os

from InstaWebBot.version import VERSION

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), 'r', encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='InstaWebBot',
    version=VERSION,
    author='Julius-W',
    description='A simple library for managing an Instagram bot as a web application.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/Julius-W/InstaBot',
    license='GPL-2.0',
    packages=['InstaWebBot'],
    python_requires='>=3.6',
    install_requires=['selenium'],
    keywords=['python', 'Instagram', 'bot', 'automation'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ]
)
