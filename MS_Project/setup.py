#!/usr/bin/env python

"""The setup script for spectra package."""

from setuptools import setup, find_packages


requirements = ["pandas>=1.1.4",
                "requests>=2.25.0",
                "matplotlib>=3.3.2",
                "click>=7.1.2",
                "werkzeug>=1.0.1",
                "flask>=1.1.2",
                "pyopenms >= 2.6.0",
                ]                   # xml is standard lib


test_requirements = ['pytest>=3', ]

setup(
    author="Group01",
    author_email='',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Group01 Spectra Package",
    entry_points={
        'console_scripts': [
            'spectra_package=spectra_package.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='spectra_package',
    name='spectra_package',
    packages=find_packages(include=['spectra_package', 'spectra_package.*']),
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.0',
    zip_safe=False,
)
