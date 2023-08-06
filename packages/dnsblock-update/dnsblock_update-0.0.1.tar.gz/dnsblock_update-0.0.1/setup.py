"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='dnsblock_update',
    version='0.0.1',
    author='Simon Schneider',
    author_email='dev@raynigon.com',
    description='Blocklist Updater for DNS Masq',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/raynigon/dnsblock-update',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    keywords='dnsmasq',
    project_urls={
        'Bug Reports': 'https://github.com/raynigon/dnsblock-update/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
    python_requires='>=3.6, <4',
    install_requires=[
        'requests',
        'pyyaml'
    ],
    extras_require={
        'dev': ['setuptools', 'wheel'],
        'test': ['coverage'],
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
