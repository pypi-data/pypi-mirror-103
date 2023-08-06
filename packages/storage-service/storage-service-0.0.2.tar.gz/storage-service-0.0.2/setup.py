import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storage-service",
    version="0.0.2",
    author="Victor Elceaninov & Dorin Musteata",
    author_email="victor.elceaninov@ebs-integrator.org, dorin.musteata@ebs-integrator.org",
    description="Storage Service is a Django + DRF package that help to work with model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebs-integrator/storage-service",
    project_urls={
        "Bug Tracker": "https://github.com/ebs-integrator/storage-service/issues",
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
    python_requires=">=3.6",
)
