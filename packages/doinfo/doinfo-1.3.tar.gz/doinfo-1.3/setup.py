from setuptools import setup, find_packages

VERSION = "1.3"
DESCRIPTION = "A simple package to lookup information via DOI"

setup(
    name="doinfo",
    version=VERSION,
    author="Tahir Murata",
    author_email="tahirmurata83@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "doi", "sci-hub", "lookup", "science", "article", "paper"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)