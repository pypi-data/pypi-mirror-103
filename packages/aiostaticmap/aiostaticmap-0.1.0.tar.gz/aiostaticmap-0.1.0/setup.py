from re import search

from setuptools import setup

with open('src/aiostaticmap/__init__.py') as f:
    version = str(search(r"__version__ = '(.*)'", f.read()).group(1))

with open('README.md') as f:
    long_description = f.read()

setup(
    name='aiostaticmap',
    version=version,
    packages=['aiostaticmap'],
    package_dir={'': 'src'},
    install_requires=[
        'Pillow >= 7.0, < 8.0',
        'aiohttp >= 3.0, < 4.0',
    ],
    # setup_requires=['pytest-runner'],
    # tests_require=[
    #     'pytest',
    #     'pytest-aiohttp',
    # ],
    url='https://github.com/mon4ter/aiostaticmap',
    license='Apache License 2.0',
    author='Christoph Lingg, Dmitry Galkin',
    author_email='christoph@komoot.de, mon4ter@gmail.com',
    description='A small, python-based library for creating map images with lines and markers.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    keywords='static map image osm aio async asyncio',
)
