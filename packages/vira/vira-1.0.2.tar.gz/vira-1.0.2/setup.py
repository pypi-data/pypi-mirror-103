from os import read
from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as rq:
        content = rq.read()
        req = content.split('\n')
    return req


def readme():
    with open('README.md') as file:
        read_data = file.read()
    return read_data


setup(
    name='vira',
    version='1.0.2',
    description='A Calculator for Calculating',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='GN Vageesh',
    author_email='vageeshgn2005@gmail.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable'
    ],
    license='MIT',
    keywords=['python', 'python3', 'details',
              'math', 'calculator', 'data', 'research', 'gui'],
    maintainer='GN Vageesh',
    maintainer_email='vageeshgn2005@gmail.com',
    download_url='https://github.com/GNVageesh/vira',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points='''
        [console_scripts]
        vira=vira.gui:gui
    '''
)
