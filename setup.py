import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bsuir_2020_python",
    version="0.0.4",
    author="Dmitriy Klebanov",
    author_email="dmitriy.klebanov@gmail.com",
    description="BSUIR labs package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmitriyklebanov/bsuir_2020_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
