import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raccgen",
    version="1.0.0",
    author="Michael Peters",
    author_email="michael@michaelpeterswa.com",
    description="Random ACCount GENerator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelpeterswa/darkthyme",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)