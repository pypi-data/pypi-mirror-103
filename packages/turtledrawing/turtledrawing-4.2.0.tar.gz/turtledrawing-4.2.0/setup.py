import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="turtledrawing",
    version="4.2.0",
    description="Draw Shapes with the Turtle Module.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="orcawhale38",
    author_email="orcawhale2008@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["shapes"],
    include_package_data=True,
    url="https://github.com/NotOrca22/learning-turtle",
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)