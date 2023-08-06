import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kowanasutil", # Replace with your own username
    version="0.0.5",
    author="kowanas",
    author_email="saramsoftware@gmail.com",
    description="kowanas utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kowanas/kowanasuti",
    project_urls={
        "Bug Tracker": "https://github.com/Kowanas/kowanasuti/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)