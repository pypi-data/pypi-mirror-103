import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    # long_description=long_description,
    long_description_content_type="text/markdown",

setuptools.setup(
    name="mugan86-openwm-api", # Replace with your own username
    version="0.0.3",
    author="Anartz Mugika Ledo",
    author_email="mugan86@gmail.com",
    description="Obtenemos el tiempo seleccionado de una ubicación",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
