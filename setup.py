try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'cuby client for python',
    'author': 'subdragon',
    'url': 'https://github.com/chenyin/cube-python.git',
    'download_url': 'https://github.com/chenyin/cube-python/zipball/master',
    'author_email': 'subdragon@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'requests'],
    'packages': ['cube'],
    'scripts': [],
    'name': 'pycube'
}

setup(**config)
