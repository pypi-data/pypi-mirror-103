import setuptools

with open("README.md", "r") as f:
    _description = f.read()

setuptools.setup(
    name="tag-formatter",
    version="1.3.0",
    author="jay3332",
    description="Tag-formatter is a Python Package designed to format strings that based on user-input.",
    long_description=_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jay3332/tag-formatter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
