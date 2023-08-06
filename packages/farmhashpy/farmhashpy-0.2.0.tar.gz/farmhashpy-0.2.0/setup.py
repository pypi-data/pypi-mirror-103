#!/usr/bin/env python


from setuptools import setup, find_packages, Extension

setup(
    name="farmhashpy",
    version="0.2.0",
    keywords=("farmhash", "google"),
    description="Google FarmHash Bindings for Python. Based on abandoned work by Veelion.",
    long_description=open("README.md", "r").read(),
    author="Isaac Elbaz",
    author_email="ielbaz@openaristos.io",
    url="https://github.com/openaristos/farmhashpy",
    packages=find_packages("src"),
    package_dir={"": "src"},
    ext_modules=[
        Extension(
            "farmhash",
            ["src/farmhash.cc", "src/python-farmhash.cc"],
            extra_compile_args=["-O4"],
        )
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
