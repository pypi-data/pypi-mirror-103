from pathlib import Path

from setuptools import setup, find_packages


if __name__ == '__main__':

    with open(Path(__file__).parent / 'README.md', encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name="deep-rec",
        version="0.0.0",
        description="PyTorch implementation of Deep Factorization Machine Models",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jaisenbe58r/deep-rec",
        author="Jaime Sendra Berenguer",
        author_email="jaimesendraberenguer@gmail.com",
        packages=find_packages(exclude=["examples", "docs"]),
    )