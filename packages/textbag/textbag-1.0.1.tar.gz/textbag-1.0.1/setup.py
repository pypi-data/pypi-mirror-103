import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="textbag",
    version="1.0.1",
    description="bag-of-words implementer and tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JacobDer/textbag",
    author="Real Python",
    author_email="jacobder9@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["textbag"],
    include_package_data=True,
    install_requires=["nltk", "pandas", "numpy"]
)
