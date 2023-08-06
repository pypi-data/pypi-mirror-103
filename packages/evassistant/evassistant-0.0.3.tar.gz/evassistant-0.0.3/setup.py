import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="evassistant",
    version="0.0.3",
    author="jeff liu",
    author_email="liuyp2080@163.com",
    description="tools for external validation of predication models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuyp2080/evassistant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
