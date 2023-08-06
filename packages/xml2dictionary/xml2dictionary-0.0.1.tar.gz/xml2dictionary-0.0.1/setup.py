import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xml2dictionary",
    version="0.0.1",
    author="Dorin Musteata & Victor Elceaninov",
    author_email="dorin.musteata@ebs-integrator.com, victor.elceaninov@ebs-integrator.com",
    description="xml2json is a package that converts any xml to json (dict).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebs-integrator/xml2dictionary",
    project_urls={
        "Bug Tracker": "https://git2.devebs.net/ebs-backend/python/packages/model-observer/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
