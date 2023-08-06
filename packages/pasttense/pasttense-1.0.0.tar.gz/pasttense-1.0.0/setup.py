import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pasttense",
    version="1.0.0",
    author="Haard Majmudar",
    author_email="haardmajmudar2827@email.com",
    description="A past tense package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Haardispro/module2",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
