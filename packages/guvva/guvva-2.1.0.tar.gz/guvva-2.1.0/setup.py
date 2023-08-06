import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guvva",
    version="2.1.0",
    author="MasterMind",
    author_email="mastermindm2rd@gmail.com",
    description="A tough programing language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.google.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)