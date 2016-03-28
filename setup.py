import os
import re
from setuptools import setup, find_packages

from codecs import open


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r', 'utf-8') as f:
        return f.read()

readme = read('README.rst')
history = read('HISTORY.rst')

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    read('idigbio/__init__.py'), re.MULTILINE).group(1)

setup(
    name='idigbio',
    version=version,
    description='Python Client for the iDigBio Search API',
    long_description=readme + "\n\n" + history,
    url='http://github.com/idigbio/idigbio-python-client/',
    license='MIT',
    author='Alex Thompson',
    author_email='godfoder@acis.ufl.edu',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests'],
    extras_require={
        "pandas": ["pandas"]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
