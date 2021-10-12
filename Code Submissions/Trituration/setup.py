"""RSH"""
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = ['setuptools>=18.0', 'biopython']


setup(
    name='rsh',
    version='0.0.1',
    description='calculate enrichment of matrix in data',
    author='Anton Tsukanov, Konstantin Ivanov, Georgii Ozhegov',
    author_email='ubercomrade@gmail.com',
    url='https://github.com/trituration/rsh',
    scripts=['restriction_sites_hider.py',],
    package_data={'rsh': ['db/restriction_enzymes_database.tsv']},
    classifiers=[
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Cython',
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=install_requires,
    python_requires='>=3.7',
)