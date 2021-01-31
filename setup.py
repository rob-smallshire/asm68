import io
import os

from setuptools import setup, find_packages


def local_file(*name):
    return os.path.join(
        os.path.dirname(__file__),
        *name)


def read(name, **kwargs):
    with io.open(
        name,
        encoding=kwargs.get("encoding", "utf8")
    ) as handle:
        return handle.read()


def read_version():
    "Read the `(version-string, version-info)` from `asm68/version.py`."
    version_file = local_file('source', 'asm68', 'version.py')
    local_vars = {}
    with open(version_file) as handle:
        exec(handle.read(), {}, local_vars)
    return (local_vars['__version__'], local_vars['__version_info__'])


LONG_DESCRIPTION = read(local_file('README.rst'), mode='rt')


INSTALL_REQUIRES = [
    'frozendict',
    'click',
    'exit_codes',
]

TESTS_REQUIRE = [
    'pytest',
    'hypothesis',
]

setup(
    name='asm68',
    python_requires='>=3.6',
    version=read_version()[0],
    packages=find_packages(),
    author='Robert Smallshire',
    author_email='robert@smallshire.org.uk',
    description='6309 assembler as an internal Python Domain Specific Language',
    license='MIT License',
    keywords='asm assembly 6809 6309 8-bit',
    url='http://github.com/rob-smallshire/asm68',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Assembly',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Assemblers',
    ],
    platforms='any',
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    setup_requires=['pytest-runner'],
    tests_require=TESTS_REQUIRE,
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': ['sphinx', 'sphinx_rtd_theme'],
    },
    entry_points={
        'console_scripts': [
            'asm68 = asm68.cli:cli',
        ],
    },
    long_description=LONG_DESCRIPTION,
)

