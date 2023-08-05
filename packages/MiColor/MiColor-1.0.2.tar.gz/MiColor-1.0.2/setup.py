import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MiColor", # Replace with your own username
    version="1.0.2",
    author="MiLang Creations",
    author_email="milangcreations@gmail.com",
    description="Manipulate console colours.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milangcreations/Color",
    project_urls={
        "Bug Tracker": "https://github.com/milangcreations/Color/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
