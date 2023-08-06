import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guvvam",
    version="2.0.0",
    author="MasterMind",
    author_email="mastermindm2rd@gmail.com",
    description="A tough programing language for mac",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/guvva/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)