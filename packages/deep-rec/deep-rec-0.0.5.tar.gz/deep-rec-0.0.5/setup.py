# from distutils.core import setup
from os.path import realpath, dirname, join
from setuptools import setup, find_packages
from pathlib import Path
import deeprec

VERSION = deeprec.__version__
PROJECT_ROOT = dirname(realpath(__file__))

REQUIREMENTS_FILE = join(PROJECT_ROOT, 'requirements.txt')

with open(REQUIREMENTS_FILE) as f:
    install_reqs = f.read().splitlines()

install_reqs.append('setuptools')


if __name__ == '__main__':

    with open(Path(__file__).parent / 'README.md', encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name="deep-rec",
        version=VERSION,
        description="PyTorch implementation of Deep Factorization Machine Models",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jaisenbe58r/deep-rec",
        author="Jaime Sendra Berenguer",
        author_email="jaimesendraberenguer@gmail.com",
        packages=find_packages(exclude=["examples", "docs"]),
        include_package_data=True,
        install_requires=install_reqs,
        platforms='any',

        classifiers=[
            'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',      # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Programming Language :: Python :: 3.7',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Scientific/Engineering :: Image Recognition',
        ],
        python_requires='>=3.6',
)