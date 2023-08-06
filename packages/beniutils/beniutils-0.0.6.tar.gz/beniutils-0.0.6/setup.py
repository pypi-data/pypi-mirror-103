version = "0.0.6"

from setuptools import setup, find_packages

setup(
    name = "beniutils",
    version = version,
    keywords="beni",
    description = "utils library for Beni",
    license = "MIT License",
    url = "https://pypi.org/project/beniutils/",
    author = "Beni",
    author_email = "benimang@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "aiohttp>=3.6.2",
        "aiofiles>=0.4.0",
        "xlrd>=1.2.0",
    ],
)