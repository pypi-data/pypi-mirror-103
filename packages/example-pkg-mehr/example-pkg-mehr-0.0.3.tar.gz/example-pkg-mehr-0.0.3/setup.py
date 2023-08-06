import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-mehr", # Replace with your own username
    version="0.0.3",
    author="mehr",
    author_email="mehr@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehr/packaging_tutorial.git",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src", "File": "src/__init__.py"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)