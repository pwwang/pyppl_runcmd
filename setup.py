# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='pyppl_runcmd',
    version='0.0.3',
    description='Allowing to run local command before and after each process for PyPPL',
    python_requires='==3.*,>=3.6.0',
    author='pwwang',
    author_email='pwwang@pwwang.com',
    license='MIT',
    entry_points={"pyppl": ["pyppl_runcmd = pyppl_runcmd"]},
    packages=[],
    package_dir={"": "."},
    package_data={},
    install_requires=['cmdy', 'pyppl==3.*'],
    extras_require={"dev": ["pytest", "pytest-cov"]},
)
