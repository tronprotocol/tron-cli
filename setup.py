import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="troncli",
    version="0.0.1",
    author="Weiyu X",
    author_email="weiyu@tron.network",
    description="A command line tool to monitor and manage tron nodes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tronprotocol/tron-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)