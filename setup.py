from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read()

setup(
    name="genrify",
    version="0.0.1",
    description="CLI tool for editing genre tags in music files",
    author="Eric Moloney",
    author_email="moloneer@tcd.ie",
    url="https://github.com/moloney1/genrify",
    install_requires=[r for r in requirements.splitlines()],
    packages=["genrify", "genrify.lib"],
    entry_points={
        "console_scripts": [
            "genrify = genrify.genrify_run:main"
        ]
    }
)
