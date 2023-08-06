import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MouseBit",
    version="0.0.1",
    author="Herumb Shandilya",
    author_email="herumbshandilya123@gmail.com",
    description="An easy to use PyTorch utility for easy DataLoader creation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krypticmouse/MouseBit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)