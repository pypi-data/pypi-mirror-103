#!/usr/bin/env python3
import os

import setuptools

version = {}
with open("pg_sql/version.py", "r") as f:
    exec(f.read(), version)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    author="Rivet Health",
    author_email="ops@rivethealth.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    description="Construct PostgreSQL SQL",
    extras_require={"dev": ["black", "isort"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="pg_sql",
    packages=setuptools.find_packages(),
    project_urls={
        "Issues": "https://github.com/rivethealth/pg-sql-py/issues",
    },
    python_requires=">3.7.0",
    url="https://github.com/rivethealth/pgsql",
    version=version["__version__"],
)
