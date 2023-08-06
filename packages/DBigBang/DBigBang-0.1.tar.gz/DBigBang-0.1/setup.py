try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Analysis of Mailman archives',
    'long_description': 'Analysis of Mailman archives',
    'long_description_content_type': 'text/x-rst',
    'author': 'Sebastian Benthall',
    'url': 'https://gitbub.com/datactive/bigbang',
    'download_url': 'https://gitbub.com/datactive/bigbang',
    'author_email': 'sb@ischool.berkeley.edu',
    'version': '0.1',
    'install_requires': [
        'beautifulsoup4',
        'chardet',
        'coverage',
        'html2text',
        'ipython',
        'jinja2',
        'jsonschema',
        'matplotlib',
        'networkx',
        'numpy',
        'pandas',
        'pytest',
        'python-dateutil',
        'python-Levenshtein',
        'pytz',
        'pyzmq',
        'tornado',
        'requests',
        'pyyaml',
        'common',
        'powerlaw'],
    'packages': ['dbigbang'],
    'scripts': [],
    'name': 'DBigBang'}

setup(**config)
