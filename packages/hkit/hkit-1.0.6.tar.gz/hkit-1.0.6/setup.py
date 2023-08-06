import setuptools

setuptools.setup(
    name="hkit",
    version="1.0.6",
    author="huangweiwei",
    author_email="geverway@gmail.com",
    description="simple tools for daily use",
    long_description="#ReadMe",
    long_description_content_type="text/markdown",
    url="https://404.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite="tests",
    python_requires='>=3.6'
)
