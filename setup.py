import os
from setuptools import setup, find_packages

PACKAGE = 'troncli'


def cat(files, join_str=''):
    """Concatenate `files` content with `join_str` between them."""
    files_content = (open(f).read() for f in files)
    return join_str.join(files_content)


def get_version(package):
    """ Extract package version without importing file
    Importing cause issues with coverage,
        (modules can be removed from sys.modules to prevent this)
    Importing __init__.py triggers importing rest and then requests too
    Inspired from pep8 setup.py
    """
    with open(os.path.join(package, '__init__.py')) as init_fd:
        for line in init_fd:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

SCRIPTS = ['tron-cli']
LONG_DESCRIPTION_FILES = ['README.md', 'CHANGELOG.md']

setup(
    name=PACKAGE,
    version=get_version(PACKAGE),
    author='Weiyu X',
    author_email='weiyu@tron.network',
    description='A command line tool to monitor and manage tron nodes.',
    long_description=cat(LONG_DESCRIPTION_FILES, u'\n\n'),
    long_description_content_type='text/markdown',
    url='https://github.com/tronprotocol/tron-cli',
    packages=find_packages(),
    scripts=SCRIPTS,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['cbox==0.5.0', 'certifi==2018.10.15', 'chardet==3.0.4', 'idna==2.7', 
        'psutil==5.4.7', 'requests==2.20.0', 'six==1.11.0', 'urllib3==1.24', 'colorama==0.4.0', 'tqdm==4.28.1'],
)