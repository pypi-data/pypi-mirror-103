import setuptools


with open("README.md") as fh:
    long_description = fh.read()


setuptools.setup(
    name="sorta",
    version="0.0.2",
    scripts=["sorta"],
    author="Jordan Patterson",
    author_email="jordanpatterson1939@gmail.com",
    descdription="Get rid of clutter on your pc. Sorta organizes your files by moving them to folders based on their filetype.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pattersonjor/sorta",
    packages=setuptools.find_packages(),
    install_requires=['getkey'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
