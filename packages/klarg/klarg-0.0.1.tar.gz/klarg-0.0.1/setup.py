from distutils.core import setup


def read_file(file_to_read: str):
    with open(file_to_read) as file:
        return file.read()


long_description = read_file("README.md")


setup(
    name="klarg",
    version="0.0.1",
    author="Tomi Adenekan",
    author_email="tominekan@outlook.com",
    description="A simple command line argument parsing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tominekan/klarg",
    project_urls={
        "Bug Tracker": "https://github.com/tominekan/klarg/issues",
        "Documentation": "https://github.com/tominekan/klarg/blob/main/DOCS.md"
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.7",
    package_dir={"": "."},
    py_modules=["klarg"]
)
