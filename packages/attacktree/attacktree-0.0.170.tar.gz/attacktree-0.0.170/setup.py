from setuptools import setup, find_packages

setup(
    name = "attacktree",
    version = "0.0.170",
    author = "hyakuhei",
    author_email = "hyakuhei@gmail.com",
    summary = "Build, analyize and render attack trees",
    description = "Describe attack-defense-attack sequences using python",
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/hyakuhei/attackTrees",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "attacktree"},
    packages=find_packages(where="attacktree"),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires = ["graphviz >=0.16"]
)