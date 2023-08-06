#!/usr/bin/env python

from distutils.core import setup


setup(
    name="nlab_essential",
    package_dir={
        "nlab": ".",
    },
    packages=[
        "nlab",
    ],
    version="0.0.0",
    license="MIT",
    description="Essential tools.",
    author="Dmitry Makarov",
    author_email="dmakarov@nanosemantics.ru",
    install_requires=[],
)