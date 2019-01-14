"""The setup.py file for Tron CLI."""

import sys


from setuptools import setup, find_packages

"""
python version check
"""
if sys.version_info < (3,7):
    sys.exit('Sorry, please update python to 3.7+ to avoid unexpected issues.')

def cat(files, join_str=''):
    """Concatenate `files` content with `join_str` between them."""
    files_content = (open(f).read() for f in files)
    return join_str.join(files_content)


PKG_NAME = 'troncli'
PKG_AUTHOR = ', '.join(['Weiyu X'])
PKG_SCRIPTS = ['tron-cli']
PKG_VERSION = '0.3.0'
PKG_REQUIRES = [
    'bleach',
    'cbox',
    'certifi',
    'chardet',
    'colorama',
    'docutils',
    'idna',
    'pkginfo',
    'psutil',
    'Pygments',
    'readme-renderer',
    'requests',
    'requests-toolbelt',
    'six',
    'tqdm',
    'urllib3',
    'webencodings'
]

PKG_DESC = 'A command line tool to monitor and manage tron nodes.'
PKG_LONG_DESC = cat(['README.md', 'CHANGELOG.md'], u'\n\n')

setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    author=PKG_AUTHOR,
    author_email='weiyu@tron.network',
    description=PKG_DESC,
    long_description=PKG_LONG_DESC,
    long_description_content_type='text/markdown',
    url='https://github.com/tronprotocol/tron-cli',
    packages=find_packages(),
    zip_safe=False,
    scripts=PKG_SCRIPTS,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=PKG_REQUIRES,
)
