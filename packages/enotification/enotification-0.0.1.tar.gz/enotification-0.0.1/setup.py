import setuptools
from setuptools import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enotification",
    version="0.0.1",
    author="DiamondI",
    author_email="920076768@qq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DiamondI/enotification",
    project_urls={
        "Bug Tracker": "https://github.com/DiamondI/enotification/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "enotification"},
    python_requires=">=3.6"
)
