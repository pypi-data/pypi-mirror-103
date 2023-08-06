import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yorumsepeti", # Replace with your own username
    version="0.0.4",
    author="Doğukan Arslan",
    author_email="dogukan997@hotmail.com",
    description="A package for fetching restaurant reviews from Yemeksepeti.com.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dgknrsln/yorumsepeti",
    project_urls={
        "Bug Tracker": "https://github.com/dgknrsln/yorumsepeti/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['selenium'],
    python_requires=">=3.6",
)