from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="darcyforchheimer",
    url="https://github.com/Hynack/darcyforchheimer",
    author="David Hinojosa",
    author_email="hynack@gmail.com",
    version="0.0.1",
    description="darcy-forchheimer parameters calculator helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["darcyforchheimer"],
    install_requires=[
        "scipy ~= 1.6",
    ],
    extras_require={
        "dev": [
            "pytest >= 6.2.3",
        ]
    },
    package_dir={"": "darcyforchheimer"},
    packages=find_packages("src", exclude=["tests"]),
)
