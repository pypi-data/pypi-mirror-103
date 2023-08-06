import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qkit",
    version="0.1.1",
    author="Ken Younge",
    author_email="kenyounge@gmail.com",
    description="Quantitative Toolkit from Quant AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KenYounge/qkit",
    packages=["qkit/", ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)