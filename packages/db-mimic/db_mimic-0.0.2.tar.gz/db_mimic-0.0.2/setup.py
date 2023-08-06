from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "package to emulate simple db functions"
LONG_DESCRIPTION = "package to emulate simple db functions: create_table, select_from_table, show_table, filter_table"

# Setting up
setup(
    name="db_mimic",
    version=VERSION,
    author="Alex Kuhn",
    author_email="<alex.kuhn1123@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "db_mimic"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)