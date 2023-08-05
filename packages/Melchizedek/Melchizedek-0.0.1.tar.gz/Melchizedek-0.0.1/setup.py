import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Melchizedek", # It should be unique name
    version="0.0.1",
    author="Hugo Six",
    author_email="hugo.six.pro@gmail.com",
    description="Hugo's Personnal package for own code reuse",
    long_description=long_description,
    long_description_content_type="text/markdown",
#    url="https://mysite.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
install_requires=[
        "seaborn"
        "matplotlib"
        "numpy==1.19.2"
        "scipy"
        "pandas"
        "scikit_learn"
        "pytest"
        "tensorflow"
    ],
    python_requires='>=3.8',
)