import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-mannerism",
    version="0.0.1",
    author="Unis Badri",
    author_email="unis.badri@elementcreativestudio.com",
    description="Test library example for pypi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/namikazebadri/PythonLibrary",
    packages=['pylib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)