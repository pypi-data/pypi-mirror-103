import setuptools

with open("README.md", "r") as fh:
    long_description_md = fh.read()

setuptools.setup(
    name="stonktrack",
    version="0.9.0",
    author="Anthony Chen",
    description="Terminal utility that can track stocks, cryptocurrencies, forexes, and more. Built with Python and urwid.",
    long_description=long_description_md,
    long_description_content_type="text/markdown",
    url="https://github.com/slightlyskepticalpotat/stonktrack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyyaml",
        "requests",
        "urwid"
    ],
    python_requires='>=3.8',
)

