import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dofpy",
    version="2.0.1",
    author="Axel Ország-Krisz Dr., Richárd Ádám Vécsey Dr.",
    author_email="dof@hyperrixel.com",
    description="Deep Model Core Output Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperrixel/dof",
    project_urls={
        "Bug Tracker": "https://github.com/hyperrixel/dof/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
