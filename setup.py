#!/usr/bin/env python3
"""
Setup script for PlusML Data Visualization package.
"""

from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt"""
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def read_readme():
    """Read README.md content"""
    with open('Readme.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='plusml-data-visualization',
    version='0.1.0',
    description='A standardized plotting framework for scientific research with consistent font, size, and output specifications',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='PlusML Team',
    author_email='contact@plusml.org',
    url='https://github.com/plusml/plusml-data-visualization',
    
    # Find all packages except tests and download script
    packages=find_packages(exclude=[
        'tests*', 
        '*.tests', 
        '*.tests.*', 
        'tests.*',
    ]),
    
    # Include non-Python files
    package_data={
        '': ['*.md', '*.txt', '*.rst'],
    },
    
    python_requires='>=3.7',
    install_requires=read_requirements(),
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
    keywords='plotting visualization scientific-research matplotlib',
    
    project_urls={
        'Bug Reports': 'https://github.com/plusml/plusml-data-visualization/issues',
        'Source': 'https://github.com/plusml/plusml-data-visualization',
        'Documentation': 'https://github.com/plusml/plusml-data-visualization#readme',
    },
)
