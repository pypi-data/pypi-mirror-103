# -*- coding: utf-8 -*-


import re
import ast
import os

from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('alipay/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


def fread(fname):
    filepath = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(filepath):
        with open(filepath) as f:
            return f.read()


setup(
    name='python-alipay',
    description='Alipay for Python',
    long_description=fread('docs/quickstart.rst'),
    license='BSD',
    packages=find_packages(),
    version=version,
    author='catroll',
    author_email='ninedoors@126.com',
    url='https://github.com/catroll/python-alipay',
    keywords=['alipay', 'alipay pay', 'alipay login', 'alipay mp', 'alipay python'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
