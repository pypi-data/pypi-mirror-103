import os
import re

from setuptools import setup

# Utils ----------------

def readf(fname):
    print(os.path.join(os.path.dirname(__file__), fname))
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

# From discord.py ------
# https://github.com/Rapptz/discord.py

def get_version(fname):
    return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', readf(fname), re.MULTILINE).group(1)
    # re.MULTILINE tells `search` to compare each line instead of the whole text.
    # \s - whitespace character
    # [\'"] - either ' or "
    # ([^\'"]*) - characters that are NOT ' or "
    # .group(1) will return the first subgroup of the match - subgroups are enclosed in `()`

# ----------------------

version = get_version('speck/__init__.py')

# Requirements ---------

install_requires = list(readf('requirements.txt').splitlines())
extras_require = {
    'docs': [
        'sphinx',
        'sphinx-press-theme'
    ]
}

# ----------------------

packages = [
    "speck",
    "speck.types",
    "speck.etc"
]
package_data = {
    '': ['LICENSE', 'README.md', 'etc/*']
}

setup(
    name = "speck-wrapper",
    version = version,
    license = "MIT",
    author = "Nevin Jose, Sachin Cherian",
    description = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README.md'),
    long_description_content_type = 'text/markdown',
    url = "https://github.com/schctl/speck",
    packages = packages,
    package_data = package_data,
    include_package_data = True,
    install_requires = install_requires,
    extras_require = extras_require,
    python_requires = ">=3.6.0"
)
