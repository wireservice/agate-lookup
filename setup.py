from setuptools import find_packages, setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='agate-lookup',
    version='0.3.2',
    description='agate-lookup adds remote lookup tables to agate.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Christopher Groskopf',
    author_email='chrisgroskopf@gmail.com',
    url='https://agate-lookup.readthedocs.org/',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'agate>=1.5.0',
        'requests>=2.9.1',
        'pyyaml>=3.11'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
        ],
        'docs': [
            'Sphinx>=1.2.2',
            'sphinx_rtd_theme>=0.1.6',
        ],
    }
)
