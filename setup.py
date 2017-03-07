from setuptools import setup, find_packages
from codecs import open
from os import path

import certbot_py

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst')
except ImportError:
    long_description = open(path.join(here, 'README.md')).read()

setup(
    name='certbot_py',
    version=certbot_py.__version__,
    description="Python module to integrate automated Let's Encrypt `certbot certonly` certificate creation into Python projects.",
    long_description=long_description,
    keywords='certbot letsencrypt ssl certificate https secure encrypt encryption',

    url='https://github.com/jaddison/certbot_py',

    author='jaddison',
    author_email='addi00+github.com@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['six'],

    entry_points={
        'console_scripts': [
            'certbot_py=certbot_py.client:main'
        ]
    },

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
)
