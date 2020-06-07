import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-gbcrawler-loalon",
    version="0.3.0",
    author="Alonso Serrano",
    author_email="bioinformatics@loalon.com",
    description="Complete GenBank parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loalon/gbcrawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)