import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yotpo-api", 
    version="0.0.1",
    author="molotov1907",
    author_email="atanasoff.yordan@gmail.com",
    description="yotpo api integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=["yotpo_api"],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        'python-dateutil'
    ],
    extras_require={
        "dev": ["pytest>=3.7", "black"],
    },
)
