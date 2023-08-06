import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyPOM-kkrenzke",
    version="0.0.0dev6",
    author="Kyler Krenzke",
    author_email="kkrenzke@gmail.com",
    description="A page object model (POM) framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kylerkrenzke/pypom",
    project_urls={
        "Bug Tracker": "https://github.com/kylerkrenzke/pypom/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    py_modules=['pypom'],
    install_requires=[
        'selenium',
    ]
)