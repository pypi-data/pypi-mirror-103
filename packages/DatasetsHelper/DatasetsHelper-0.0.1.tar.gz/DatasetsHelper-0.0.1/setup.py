import setuptools
# setuptools.setup()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DatasetsHelper", # Replace with your own username
    version="0.0.1",
    author="konosubakonoakua",
    author_email="ailike_meow@qq.com",
    description="A package to get normalization parameters used in different datasets like imagenet, cifar etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/konosubakonoakua/DatasetsNormalizationParameters",
    project_urls={
        "Bug Tracker": "https://github.com/konosubakonoakua/DatasetsNormalizationParameters/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    package_data={'': ['data/*.json']},
)