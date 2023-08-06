import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gamma-futures-BT", # Replace with your own username
    version="0.0.5",
    author="Gaurav Singh",
    author_email="gauravsingh0109@gmail.com",
    description="A small backtesting package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)