# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:34:04 2019

@author: nelson
"""

from setuptools import find_packages, setup
# from distutils.core import setup

setup(
    name='NSFopen',
    version='1.1.11',
    description='Read data and parameters from Nanosurf NID files',
    author='Nanosurf',
    author_email='scripting@nanosurf.com',
    url="https://www.nanosurf.com",
    packages = find_packages(),
    include_package_data = True,
    package_data = {
        'example': ['*.nid',
                    'Calculate_Roughness/*.*',
                    'Lateral_Force/*.*',
                    'Plotting_Data/*.*']},
    # install_requires=["numpy","time","pandas"]
    # package_dir = {'NSFopen':'NSFopen',
    #                'NSFopen.read':'NSFopen//read',
    #                'NSFopen.process':'NSFopen//process'},
    # packages=['NSFopen','NSFopen.read','NSFopen.process']
    )
