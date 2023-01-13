from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="advent-of-code",
    version="1.0.0",
    author="Ethan Lu",
    author_email="fang.lu@gmail.com",
    description="Advent of Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>3.9',
    packages=find_packages(),
    install_requires=[
        "argparse"
    ],
    entry_points={
        'console_scripts': [
            'aoc = adventofcode.app:main'
        ]
    }
)
