from setuptools import setup, find_packages

setup(
    name="pixel_reshaper",
    version="0.0.2",
    author="Jeremy Crow",
    author_email="jeremy.crow95@gmail.com",
    description="A package to structure and convert image datasets from .csv to .png representation for classification",
    url="https://github.com/je-c/pixel_reshaper",
    packages=find_packages(exclude=["tests*"]),
    package_data={"pixel_reshaper": ["data/*.csv"]},
    install_requires=["numpy", "pandas"],
    setup_requires=["wheel"],
    python_requires=">=3",
    license="MIT License",
    keywords=[
        "easy image data unpacking",
        "csv to png",
        "image classification",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
    ],
    #long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
)