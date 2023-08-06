import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tialgo",
    version="0.0.2",
    description="Algorithm SDK for TencentCloud TIONE",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://cloud.tencent.com",
    author="liang chen",
    author_email="chenliang@tencent.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["tialgo"],
    include_package_data=True,
    install_requires=["pandas", "matplotlib", "numpy"],
)

