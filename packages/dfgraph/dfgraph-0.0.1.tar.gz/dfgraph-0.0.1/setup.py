import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dfgraph", # Replace with your own username
    version="0.0.1",
    author="Willi Zschiebsch",
    author_email="willi.w.zschiebsch@web.de",
    description="A simple graph database system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willi-z/dfgraph",
    project_urls={
        "Bug Tracker": "https://github.com/willi-z/dfgraph/issues",
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